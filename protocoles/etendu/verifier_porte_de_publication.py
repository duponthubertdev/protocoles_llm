"""
Porte de publication : l'etat local du depot est-il coherent avec le perimetre declare ?

Deux façons de s'en servir, et une seule logique.

1. **Comme bibliotheque**, depuis le controle statique d'un projet -- cas normal. Le perimetre d'un
   projet est reparti sur des cles qui lui sont propres ; seul son script sait les aplatir.

       from verifier_porte_de_publication import controler_la_porte
       manquements += controler_la_porte(racine, manifeste, perimetre, conventions)

2. **En ligne de commande**, pour un projet qui ne fournit aucun controle statique et dont le
   manifeste declare un perimetre a plat sous la cle `perimetre` :

       python verifier_porte_de_publication.py <chemin_du_manifeste>

L'agent publie sa branche quand cette porte l'y autorise, jamais parce qu'il estime que tout s'est
bien passe. Un agent qui juge son propre travail le juge avec l'appareil qui vient eventuellement de
se tromper : c'est l'invariant I1 -- le verdict ne vient jamais de l'agent -- applique a la derniere
operation de la conduite.

CE QUE CETTE PORTE N'ATTESTE PAS, et qu'il ne faut pas lui preter :

- que les validations par execution ont eu lieu. Elle empeche de publier un etat incoherent, elle ne
  remplace pas la definition of done ;
- que TOUS les commits de la branche appartiennent au perimetre declare. Elle lit l'index et l'arbre
  de travail, jamais l'historique. Et elle ne peut pas le faire : le manifeste ne declare que ce que
  le controle statique doit inspecter, alors qu'une conduite touche legitimement des abstractions
  partagees qu'aucune cle ne couvre, et les referentiels que P7 doit alimenter. Comparer l'historique
  au manifeste produirait un refus sur une conduite parfaitement conforme.

La revue du contenu de la branche reste donc humaine, et elle a son moment : l'ouverture de la demande
de fusion, reservee au proprietaire du depot. Publier une branche de sujet ne la fusionne pas.

Codes de sortie du mode ligne de commande :
    0 : la branche peut etre poussee
    1 : au moins un manquement
    2 : manifeste absent, illisible ou incomplet
    4 : porte indecidable -- git n'a pas repondu
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from json import JSONDecodeError
from pathlib import Path


CLES_MANIFESTE_POUR_LA_PORTE = ("racine_depot", "contrat_de_correction", "branche_du_sujet")

TITRE_NOTES_DEXECUTION = "Notes d'exécution"
STATUT_FICHE_OUVERTE = "OUVERTE"
MOTIF_STATUT_DE_FICHE = re.compile(r"^\*\*Statut :\*\*\s*(OUVERTE|CLOSE)\s*$", re.MULTILINE)

# Champs du format de fiche fixe par le gabarit de plan. Un bloc de niveau 3 qui n'en porte AUCUN
# n'est pas une fiche : la section des notes d'execution accueille legitimement d'autres
# sous-sections -- contexte, recapitulatif, renvoi. Sans ce filtre, chacune etait lue comme une fiche
# sans statut, et la porte refusait un document correct. Constate deux fois sur une meme conduite.
MOTIF_CHAMP_DE_FICHE = re.compile(
    r"^\*\*(Statut|Symptôme|Preuves|Hypothèse|Contre-indication|Classe|Tentative|Cause|Correction"
    r"|Résultat|Surface d'écriture autorisée) :?\*\*", re.MULTILINE)


@dataclass(frozen=True)
class Conventions:
    """
    Ce que la porte doit savoir du depot, et que le protocole ne connait pas.

    Ces trois valeurs viennent de l'annexe de projet : A3 pour les branches, A6 pour les artefacts
    operationnels globaux. Les defauts couvrent le cas ordinaire ; un projet qui s'en ecarte les
    fournit.
    """

    branches_principales: tuple[str, ...] = ("main", "master")
    motif_branche_de_sujet: re.Pattern = re.compile(r"^(feat|fix|docs|chore)/\d+-[a-z0-9-]+$")
    artefacts_operationnels_globaux: tuple[str, ...] = field(default=())


@dataclass(frozen=True)
class Manquement:
    """Un constat de non-conformite, rattache a son controle et a son objet."""

    controle: str
    chemin: str
    detail: str


class PorteIndecidable(Exception):
    """git n'a pas repondu : la porte ne peut ni autoriser ni refuser."""


class ManifesteInvalide(Exception):
    """Le manifeste ne permet pas de lancer la porte."""


def lire_git(racine: Path, arguments: list[str]) -> str:
    """Execute une commande git en LECTURE SEULE et retourne sa sortie standard."""
    resultat = subprocess.run(
        ["git", *arguments],
        cwd=racine, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if resultat.returncode != 0:
        raise PorteIndecidable(f"git {' '.join(arguments)} : {resultat.stderr.strip()}")
    return resultat.stdout


def lire_le_statut(racine: Path) -> list[tuple[str, str]]:
    """
    Retourne l'etat du depot sous forme de couples (etat, chemin).

    Deux options ne sont pas negociables. `--untracked-files=all` empeche git de condenser un dossier
    entierement non suivi en une seule entree : sans elle, un fichier declare par le manifeste dont le
    dossier parent est neuf serait annonce sous son ANCETRE, que la comparaison de perimetre ne
    reconnaitrait pas -- le fichier passerait alors inapercu. `-z` supprime le quoting et
    l'echappement des chemins, qui rendent le format lisible mais non analysable.
    """
    brut = lire_git(racine, ["status", "--porcelain", "-z", "--untracked-files=all"])
    entrees = brut.split("\0")
    statut = []
    index = 0
    while index < len(entrees):
        entree = entrees[index]
        if entree:
            etat, chemin = entree[:2], entree[3:]
            statut.append((etat, chemin))
            # Un renommage ou une copie fait suivre l'ancien chemin dans une entree distincte. Les
            # DEUX colonnes sont testees : un renommage peut etre porte par l'index comme par l'arbre
            # de travail, et n'examiner que la premiere ferait lire l'ancien chemin comme une entree.
            if "R" in etat or "C" in etat:
                index += 1
        index += 1
    return statut


def retirer_les_blocs_de_code(texte: str) -> str:
    """
    Retire les blocs delimites par des triples accents graves.

    Un plan porte le gabarit d'une fiche dans un bloc de code, en fin de section. Sans ce retrait, ce
    gabarit serait compte comme une fiche reelle et le controle signalerait une fiche sans statut sur
    un document parfaitement conforme.
    """
    return re.sub(r"```.*?```", "", texte, flags=re.DOTALL)


def extraire_les_notes_dexecution(contrat: str) -> str | None:
    """
    Retourne la section des notes d'execution, ou None si elle est absente.

    L'absence et la vacuite sont deux etats distincts : une section vide est un constat, une section
    absente est un oubli. Le titre est cherche en DEBUT DE LIGNE, faute de quoi la simple mention
    « Notes d'execution » dans la conduite recopiee suffirait a faire croire que la section existe.
    """
    marqueur = f"\n## {TITRE_NOTES_DEXECUTION}"
    debut = contrat.find(marqueur)
    if debut == -1:
        return None
    fin = contrat.find("\n## ", debut + 1)
    section = contrat[debut:] if fin == -1 else contrat[debut:fin]
    return retirer_les_blocs_de_code(section)


def controler_les_fiches_dexecution(racine: Path, document_relatif: str) -> list[Manquement]:
    """
    Verifie qu'aucune fiche d'echec ne reste ouverte, et qu'aucune ne se tait sur son statut.

    Le statut est un champ structure, et non une formulation libre : une fiche redigee autrement, ou
    simplement laissee incomplete, passerait sinon inapercue.

    Le controle est fait FICHE PAR FICHE. Un comptage global se laisserait compenser : une fiche
    portant deux statuts couvrirait une fiche n'en portant aucun, et le total resterait juste.

    UN BLOC DE NIVEAU 3 N'EST PAS FORCEMENT UNE FICHE. La section des notes d'execution accueille
    legitimement d'autres sous-sections. Un bloc ne portant aucun champ du format de fiche est donc
    lu comme de la prose et ignore.

    Limite connue, et assumee : une fiche depouillee de TOUS ses champs -- y compris son symptome et
    sa classe -- echapperait au controle. Ce ne serait plus une fiche que son propre lecteur
    reconnaitrait.
    """
    document = racine / document_relatif
    if not document.exists():
        return [Manquement("document du contrat introuvable", document_relatif,
                           "regle N10 : un controle sans cible echoue")]

    notes = extraire_les_notes_dexecution(document.read_text(encoding="utf-8-sig"))
    if notes is None:
        return [Manquement(
            "section des notes d'execution absente", document_relatif,
            f"aucune section « ## {TITRE_NOTES_DEXECUTION} », que le gabarit rend obligatoire")]

    manquements = []
    for bloc in re.split(r"^### ", notes, flags=re.MULTILINE)[1:]:
        if not MOTIF_CHAMP_DE_FICHE.search(bloc):
            continue
        titre = bloc.splitlines()[0].strip() if bloc.strip() else "<fiche sans titre>"
        statuts = MOTIF_STATUT_DE_FICHE.findall(bloc)
        if len(statuts) != 1:
            manquements.append(Manquement(
                "fiche sans statut unique", document_relatif,
                f"« {titre} » declare {len(statuts)} statut(s), attendu exactement 1"))
        elif statuts[0] == STATUT_FICHE_OUVERTE:
            manquements.append(Manquement(
                "fiche d'execution ouverte", document_relatif,
                f"« {titre} » porte {STATUT_FICHE_OUVERTE}"))
    return manquements


def controler_la_branche(
        racine: Path,
        branche_declaree: str | None,
        conventions: Conventions) -> list[Manquement]:
    """
    Verifie que la branche courante est bien celle du sujet.

    Les controles sont INDEPENDANTS, et non enchaines : declarer une branche dans le manifeste ne
    dispense pas de la convention de nommage, sans quoi la cle deviendrait un moyen de contourner la
    regle qu'elle est censee preciser. La convention prouve la FORME d'une branche de sujet ; elle ne
    prouve jamais qu'il s'agit de la branche de CE ticket, et c'est la cle qui l'etablit.
    """
    manquements = []
    branche = lire_git(racine, ["rev-parse", "--abbrev-ref", "HEAD"]).strip()

    if not branche_declaree:
        manquements.append(Manquement(
            "branche du sujet non declaree", "branche_du_sujet",
            "cle obligatoire pour publier : la convention de nommage ne rattache pas la branche"
            " au ticket"))
    if branche == "HEAD":
        manquements.append(Manquement(
            "publication depuis un HEAD detache", branche,
            "aucune branche courante : la publication exige une branche de sujet"))
    if branche in conventions.branches_principales:
        manquements.append(Manquement(
            "publication depuis une branche principale", branche,
            "la publication n'est autorisee que depuis une branche de sujet"))
    if branche_declaree and branche != branche_declaree:
        manquements.append(Manquement(
            "branche differente de celle declaree", branche,
            f"le manifeste declare {branche_declaree}"))
    if branche != "HEAD" and not conventions.motif_branche_de_sujet.match(branche):
        manquements.append(Manquement(
            "nom de branche hors convention", branche,
            f"attendu {conventions.motif_branche_de_sujet.pattern}"))
    return manquements


def controler_la_proprete_du_perimetre(
        racine: Path,
        perimetre: list[str],
        conventions: Conventions) -> list[Manquement]:
    """
    Verifie que le perimetre declare est entierement commite, et que rien de suivi ne bouge ailleurs.

    Le critere est « le PERIMETRE est propre », et non « l'arbre de travail est propre ». Exiger un
    arbre entierement propre bloquerait l'agent pour des fichiers qui ne le concernent pas -- le
    travail non suivi d'un autre chantier, par exemple. Le risque reel est de publier un etat qui ne
    correspond pas a ce qui a ete valide, et ce risque ne porte que sur le perimetre declare.

    Toutes les entrees sont normalisees en barres obliques : un manifeste ecrit avec des barres
    inverses ne correspondrait a aucun chemin retourne par git, et le perimetre paraitrait vide.
    """
    entrees = [Path(entree).as_posix() for entree in perimetre]
    manquements = []
    for etat, chemin in lire_le_statut(racine):
        if chemin in conventions.artefacts_operationnels_globaux:
            continue
        non_suivi = etat == "??"
        dans_le_perimetre = any(
            chemin == entree or chemin.startswith(entree.rstrip("/") + "/") for entree in entrees)
        if non_suivi and not dans_le_perimetre:
            continue
        manquements.append(Manquement(
            "perimetre non commite", chemin,
            "fichier non commite dans le perimetre declare"
            if dans_le_perimetre else "fichier suivi modifie hors du perimetre declare"))
    return manquements


def controler_la_porte(
        racine: Path,
        manifeste: dict,
        perimetre: list[str],
        conventions: Conventions | None = None) -> list[Manquement]:
    """
    Enchaine les quatre controles de la porte et retourne la liste complete des manquements.

    Le dossier du document portant le contrat de correction est ajoute au perimetre : c'est le
    dossier du chantier, et ses artefacts de phase doivent etre commites au meme titre que le code.
    """
    conventions = conventions or Conventions()
    manquements = []

    # La racine declaree doit etre la racine REELLE du depot. Depuis un sous-dossier, git continue de
    # produire des chemins relatifs au sommet, alors que le perimetre serait interprete relativement
    # au sous-dossier : les deux ne se rencontreraient jamais, et tout paraitrait propre.
    sommet = Path(lire_git(racine, ["rev-parse", "--show-toplevel"]).strip()).resolve()
    if sommet != racine.resolve():
        manquements.append(Manquement(
            "racine declaree differente de la racine du depot", racine.as_posix(),
            f"git place le depot en {sommet.as_posix()}"))

    contrat = manifeste["contrat_de_correction"]
    perimetre_complet = [Path(contrat).parent.as_posix(), *perimetre]

    return (
        manquements
        + controler_la_branche(racine, manifeste.get("branche_du_sujet"), conventions)
        + controler_la_proprete_du_perimetre(racine, perimetre_complet, conventions)
        + controler_les_fiches_dexecution(racine, contrat)
    )


def lire_manifeste(chemin_manifeste: Path) -> dict:
    """Lit le manifeste et verifie qu'il porte les cles que la porte exige."""
    try:
        with chemin_manifeste.open(encoding="utf-8-sig") as fichier:
            manifeste = json.load(fichier)
    except JSONDecodeError as erreur:
        raise ManifesteInvalide(
            f"JSON invalide ligne {erreur.lineno} colonne {erreur.colno}") from erreur
    except OSError as erreur:
        raise ManifesteInvalide(f"illisible ({erreur})") from erreur

    attendues = (*CLES_MANIFESTE_POUR_LA_PORTE, "perimetre")
    cles_absentes = [cle for cle in attendues if cle not in manifeste]
    if cles_absentes:
        raise ManifesteInvalide(
            f"cles absentes : {', '.join(cles_absentes)}. En ligne de commande, la porte exige un"
            " perimetre a plat ; un projet dont le perimetre est reparti sur plusieurs cles appelle"
            " controler_la_porte depuis son propre controle statique")
    return manifeste


def afficher(manquements: list[Manquement]) -> None:
    """Ecrit les manquements sur la sortie d'erreur."""
    for manquement in manquements:
        print(f"KO | {manquement.controle} | {manquement.chemin} | {manquement.detail}",
              file=sys.stderr)
    print(f"KO -- {len(manquements)} manquement(s). La branche ne peut pas etre poussee.",
          file=sys.stderr)


def main() -> int:
    """Point d'entree du mode ligne de commande."""
    if len(sys.argv) != 2:
        print("Usage : python verifier_porte_de_publication.py <chemin_du_manifeste>",
              file=sys.stderr)
        return 2

    try:
        manifeste = lire_manifeste(Path(sys.argv[1]))
    except ManifesteInvalide as erreur:
        print(f"Erreur -- manifeste inexploitable : {erreur}", file=sys.stderr)
        return 2

    racine = Path(manifeste["racine_depot"])
    try:
        # HEAD est lu AVANT et APRES : s'il change entre-temps, ce qui a ete controle n'est plus ce
        # qui serait pousse, et attester le nouveau SHA serait un faux vert.
        sha_avant = lire_git(racine, ["rev-parse", "HEAD"]).strip()
        manquements = controler_la_porte(racine, manifeste, manifeste["perimetre"])
        if lire_git(racine, ["rev-parse", "HEAD"]).strip() != sha_avant:
            manquements.append(Manquement(
                "HEAD a change pendant le controle", sha_avant,
                "l'etat controle n'est plus l'etat courant : rejouer la porte"))
    except PorteIndecidable as erreur:
        print(f"Erreur -- porte indecidable : {erreur}", file=sys.stderr)
        return 4

    if manquements:
        afficher(manquements)
        return 1

    print(f"OK -- porte franchie. SHA autorise : {sha_avant}")
    print("Ce SHA doit encore etre HEAD au moment du push. Sinon, rejouer la porte.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
