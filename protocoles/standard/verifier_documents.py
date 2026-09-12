"""
Controle des documents du protocole standard.

Il prend le document de conduite, en deduit ses trois compagnons par leur nom, lit son canon dans
`protocole.md` qui vit a cote de lui, et verifie ce qui se verifie sans jugement :

    1. les sections de chaque document existent, DANS L'ORDRE, et aucune n'est vide ;
    2. la premiere entree de la surface resout vers le document de conduite ;
    3. le plan nomme ce meme document de conduite, par un chemin absolu qui resout vers lui ;
    4. la conduite apres echec est IDENTIQUE au canon, ligne a ligne ;
    5. aucun bloc des squelettes ne subsiste, la liste etant extraite des squelettes eux-memes ;
    6. les notes portent soit la mention « Aucun echec. » seule, soit des entrees, jamais les deux ;
    7. chaque entree porte exactement un statut, pris dans les deux valeurs admises ;
    8. la chaine amont est complete : un plan suppose une analyse, une analyse suppose des
       observations ;
    9. chaque chemin touche depuis le commit de depart appartient a la surface declaree, ou aux
       sorties techniques explicitement tolerees.

Il ne juge ni le code livre, ni la pertinence de ce qui est ecrit. Des documents conformes attestent
que la conduite a ete tracee, jamais que le travail est bon.

TROIS CHOIX DE CONCEPTION, explicites et non subis.

Le canon est LU, et non recopie dans ce script. Une seconde copie du bloc vieillirait sans que rien
ne le signale, et le controle finirait par verifier une conduite que le protocole ne prescrit plus.
La contrepartie est assumee : le script depend de `protocole.md`, et son absence sort en code
3.

La liste des blocs a remplir est EXTRAITE des squelettes, et non devinee par un motif. Une
heuristique laissait passer les blocs qui ressemblent a des valeurs -- `<verdict>`, `<nom>` --
c'est-a-dire ceux qu'on oublie le plus facilement.

L'ABSENCE d'un compagnon n'est pas un manquement en soi : une conduite peut legitimement s'arreter
avant de produire un plan. Ce qui est un manquement, c'est un maillon manquant au milieu de la
chaine -- un plan sans analyse, une analyse sans observations. La chaine se controle, pas la
completude.

Codes de sortie :

    0 : aucun manquement
    1 : au moins un manquement
    2 : argument absent, mal nomme, ou fichier illisible
    3 : document, canon ou dependance du controle introuvable ou inutilisable

Le code 3 est distinct du 0 a dessein. Un controle qui repondrait « aucun manquement » parce qu'il
n'a rien trouve a examiner serait un faux vert, et c'est le plus dangereux : il se presente comme une
preuve.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

CANON = "protocole.md"

SECTIONS_DE_LA_CONDUITE = (
    "## 1. Surface d'écriture",
    "## 2. Départ",
    "## 3. Cartographie",
    "## 4. Cadrage",
    "## 5. Conduite après un échec",
    "## 6. Notes d'exécution",
    "## 7. Clôture",
)

SECTIONS_DE_L_ANALYSE = (
    "## Faits décisionnels et leur statut",
    "## Décisions",
    "## Divergences avec le cadrage",
    "## Fichiers touchés",
)

TITRE_DU_DISPOSITIF = "## Dispositif"
TITRE_DU_RETRAIT = "## Retrait des artefacts temporaires"
PREFIXE_D_ETAPE = "## Étape "
RENVOI_DU_PLAN = "Contrat de correction et notes d'exécution :"

MARQUEUR_CONDUITE_DEBUT = "<!-- CONDUITE APRES ECHEC : DEBUT -->"
MARQUEUR_CONDUITE_FIN = "<!-- CONDUITE APRES ECHEC : FIN -->"
MARQUEUR_SQUELETTES_DEBUT = "<!-- SQUELETTES : DEBUT -->"
MARQUEUR_SQUELETTES_FIN = "<!-- SQUELETTES : FIN -->"

AUCUN_ECHEC = "Aucun échec."
STATUTS_ADMIS = ("clos", "arrêt rendu au propriétaire")

NOM_DE_LA_CONDUITE = re.compile(r"^conduite_(?P<theme>.+)\.md$")
COMPAGNONS = ("observations", "analyse", "plan")

BLOC_A_REMPLIR = re.compile(r"<(?!!--)[^<>\n]{1,200}>")
TITRE_DE_SECTION = re.compile(r"^## .+$", re.MULTILINE)
ENTREE = re.compile(r"^### ", re.MULTILINE)
LIGNE_DE_STATUT = re.compile(r"^\s*[-*]?\s*\*{0,2}Statut\*{0,2}\s*:\s*(.*)$", re.MULTILINE)
PUCE = re.compile(r"^\s*[-*]\s+(.+)$", re.MULTILINE)
CHEMIN_ENTRE_BACKTICKS = re.compile(r"`([^`]+)`")
PREFIXE_COMMIT_DE_DEPART = "- Commit de départ :"
PREFIXE_SORTIES_TECHNIQUES = (
    "- Fichiers qu'une exécution modifie sans qu'ils appartiennent à un périmètre :"
)


class CibleIntrouvable(Exception):
    """Une cible declaree est absente du disque. Elle fait echouer le controle, jamais passer."""


class ArgumentInvalide(Exception):
    """L'appel est mal forme. Ce n'est pas un manquement des documents."""


class ControleImpossible(Exception):
    """Une dependance du controle est absente ou inutilisable : le controle ne peut pas conclure."""


def lire(chemin: Path) -> str:
    if not chemin.is_file():
        raise CibleIntrouvable(str(chemin))
    return chemin.read_text(encoding="utf-8")


def extraire_entre(texte: str, debut: str, fin: str, quoi: str) -> str:
    """Retourne ce que deux marqueurs encadrent, marqueurs exclus."""
    i = texte.find(debut)
    j = texte.find(fin, i + 1) if i != -1 else -1
    if i == -1 or j == -1:
        raise CibleIntrouvable(f"{quoi} : marqueurs absents du canon")
    return texte[i + len(debut):j]


def blocs_des_squelettes(canon: str) -> list[str]:
    """Retourne les blocs a remplir des quatre squelettes, sans doublon."""
    squelettes = extraire_entre(
        canon, MARQUEUR_SQUELETTES_DEBUT, MARQUEUR_SQUELETTES_FIN, "squelettes"
    )
    trouves: list[str] = []
    for bloc in BLOC_A_REMPLIR.findall(squelettes):
        if bloc not in trouves:
            trouves.append(bloc)
    if not trouves:
        raise CibleIntrouvable("squelettes : aucun bloc a remplir trouve dans le canon")
    return trouves


def normaliser(bloc: str) -> list[str]:
    """Retourne les lignes non vides du bloc, sans blanc de fin, pour une comparaison au canon."""
    return [ligne.rstrip() for ligne in bloc.replace("\r\n", "\n").split("\n") if ligne.strip()]


def resout_vers(declare: str, attendu: Path) -> bool:
    """Dit si un chemin declare designe bien le fichier attendu, casse comprise."""
    chemin = Path(declare)
    if not chemin.is_absolute():
        return False
    return os.path.normcase(str(chemin.resolve())) == os.path.normcase(str(attendu.resolve()))


def executer_git(dossier: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    """Execute Git sans shell et retourne sa sortie brute, necessaire aux listes separees par NUL."""
    try:
        return subprocess.run(
            ["git", "-C", str(dossier), *arguments],
            capture_output=True,
            check=False,
        )
    except OSError as erreur:
        raise ControleImpossible(f"git est indisponible : {erreur}") from erreur


def sortie_git(acheve: subprocess.CompletedProcess[bytes], commande: str) -> bytes:
    """Retourne stdout quand Git a reussi ; sinon le controle s'arrete avec son diagnostic."""
    if acheve.returncode == 0:
        return acheve.stdout
    erreur = acheve.stderr.decode("utf-8", errors="replace").strip()
    raise ControleImpossible(f"{commande} a echoue : {erreur or 'aucun diagnostic'}")


def chemins_nuls(sortie: bytes) -> set[str]:
    """Decode une liste de chemins Git separes par NUL, sans dependre de core.quotepath."""
    return {
        chemin.decode("utf-8", errors="surrogateescape").replace("\\", "/")
        for chemin in sortie.split(b"\0")
        if chemin
    }


def positions(texte: str, titres: tuple[str, ...]) -> dict[str, int]:
    """Retourne la position de chaque titre present, cherche en debut de ligne."""
    trouvees = {}
    for titre in titres:
        position = f"\n{texte}".find(f"\n{titre}")
        if position != -1:
            trouvees[titre] = position
    return trouvees


def corps(texte: str, titre: str, connues: dict[str, int]) -> str:
    """Retourne le corps d'une section, du titre jusqu'a la section connue suivante."""
    debut = connues[titre]
    suivantes = [p for p in connues.values() if p > debut]
    fin = min(suivantes) if suivantes else len(texte) + 1
    return f"\n{texte}"[debut + len(titre) + 1:fin]


def controler_les_sections(document: str, texte: str, titres: tuple[str, ...]) -> list[str]:
    """
    Verifie que les sections attendues existent, dans l'ordre, et qu'aucune n'est vide.

    L'absence et la vacuite sont deux etats distincts : une section supprimee est un ecart au
    squelette, une section laissee vide est indiscernable d'un oubli. Le protocole impose d'y ecrire
    « Sans objet » et sa raison plutot que de la laisser blanche.
    """
    manquements = []
    connues = positions(texte, titres)

    for titre in titres:
        if titre not in connues:
            manquements.append(f"{document} : section absente -- {titre}")

    presentes = [titre for titre in titres if titre in connues]
    rencontrees = sorted(presentes, key=lambda titre: connues[titre])
    if presentes != rencontrees:
        manquements.append(
            f"{document} : sections dans le desordre -- rencontrees "
            + " puis ".join(rencontrees)
        )

    for titre in presentes:
        if not corps(texte, titre, connues).strip():
            manquements.append(f"{document} : section vide -- {titre}")
    return manquements


def controler_la_surface(texte: str, conduite: Path) -> list[str]:
    """
    Verifie que la premiere entree de la surface RESOUT vers le document de conduite.

    Ce document est ecrit du premier au dernier pas. Absent de la surface, il rendrait la conduite
    fautive des son premier mot -- et le manquement serait invisible, puisque c'est le document qui
    porte la declaration qui manquerait a la declaration.

    Comparer les seuls noms de fichier ne suffit pas : un homonyme situe ailleurs passerait.
    """
    titre = SECTIONS_DE_LA_CONDUITE[0]
    connues = positions(texte, SECTIONS_DE_LA_CONDUITE)
    if titre not in connues:
        return []
    puces = PUCE.findall(corps(texte, titre, connues))
    if not puces:
        return ["conduite : surface d'ecriture sans aucune entree"]

    declaree = puces[0].strip().strip("`\"'").strip()
    if not resout_vers(declaree, conduite):
        return [
            "conduite : la premiere entree de la surface ne resout pas vers ce document. "
            f"Declaree « {declaree} », controle « {conduite.resolve()} »"
        ]
    return []


def valeur_de_depart(texte: str, prefixe: str) -> str | None:
    """Retourne la valeur d'une ligne fermee de la section Depart."""
    for ligne in texte.splitlines():
        if ligne.startswith(prefixe):
            return ligne[len(prefixe):].strip()
    return None


def relatif_au_depot(declare: str, racine: Path) -> str | None:
    """Normalise un chemin absolu en chemin Git, ou refuse ce qui sort de la racine."""
    chemin = Path(declare)
    if not chemin.is_absolute():
        return None
    try:
        relatif = chemin.resolve().relative_to(racine.resolve())
    except (OSError, ValueError):
        return None
    return os.path.normcase(relatif.as_posix()).replace("\\", "/")


def controler_les_chemins_git(texte: str, conduite: Path) -> list[str]:
    """Verifie que tout chemin visible par Git depuis le depart appartient a la surface."""
    manquements: list[str] = []

    racine_brute = sortie_git(
        executer_git(conduite.parent, "rev-parse", "--show-toplevel"),
        "git rev-parse --show-toplevel",
    ).decode("utf-8", errors="surrogateescape").strip()
    racine = Path(racine_brute).resolve()
    if relatif_au_depot(str(conduite.resolve()), racine) is None:
        raise ControleImpossible(f"le document de conduite est hors de la racine Git {racine}")

    depart = valeur_de_depart(texte, PREFIXE_COMMIT_DE_DEPART)
    if not depart:
        return ["git : commit de depart absent"]
    depart = depart.strip("`\"'").strip()
    commit_valide = executer_git(racine, "cat-file", "-e", f"{depart}^{{commit}}")
    if commit_valide.returncode != 0:
        return [f"git : commit de depart invalide -- {depart}"]
    ancetre = executer_git(racine, "merge-base", "--is-ancestor", depart, "HEAD")
    if ancetre.returncode != 0:
        return [f"git : le commit de depart n'est pas un ancetre de HEAD -- {depart}"]

    titre_surface = SECTIONS_DE_LA_CONDUITE[0]
    connues = positions(texte, SECTIONS_DE_LA_CONDUITE)
    if titre_surface not in connues:
        return []
    surface: set[str] = set()
    for puce in PUCE.findall(corps(texte, titre_surface, connues)):
        declare = puce.strip().strip("`\"'").strip()
        relatif = relatif_au_depot(declare, racine)
        if relatif is None:
            manquements.append(f"git : chemin de surface relatif ou hors depot -- {declare}")
        else:
            surface.add(relatif)

    sorties = valeur_de_depart(texte, PREFIXE_SORTIES_TECHNIQUES)
    techniques: set[str] = set()
    if sorties is None:
        manquements.append("git : declaration des sorties techniques absente")
    elif sorties.strip().lower() != "aucun":
        declares = CHEMIN_ENTRE_BACKTICKS.findall(sorties)
        if not declares:
            manquements.append(
                "git : sorties techniques sans chemin absolu place entre backticks"
            )
        for declare in declares:
            relatif = relatif_au_depot(declare.strip(), racine)
            if relatif is None:
                manquements.append(
                    f"git : sortie technique relative ou hors depot -- {declare.strip()}"
                )
            else:
                techniques.add(relatif.rstrip("/"))

    touches: set[str] = set()
    commits = sortie_git(
        executer_git(racine, "rev-list", "--reverse", f"{depart}..HEAD"),
        "git rev-list",
    ).decode("ascii", errors="strict").splitlines()
    for commit in commits:
        touches |= chemins_nuls(
            sortie_git(
                executer_git(
                    racine,
                    "diff-tree",
                    "--no-commit-id",
                    "--name-only",
                    "-m",
                    "-r",
                    "-z",
                    commit,
                ),
                "git diff-tree",
            )
        )
    touches |= chemins_nuls(
        sortie_git(
            executer_git(racine, "diff", "--name-only", "-z", "HEAD", "--"),
            "git diff",
        )
    )
    touches |= chemins_nuls(
        sortie_git(
            executer_git(racine, "ls-files", "--others", "--exclude-standard", "-z"),
            "git ls-files --others",
        )
    )

    for touche in sorted(touches):
        normalise = os.path.normcase(touche).replace("\\", "/")
        technique = any(
            normalise == autorise or normalise.startswith(f"{autorise}/")
            for autorise in techniques
        )
        if normalise not in surface and not technique:
            manquements.append(f"git : chemin touche hors surface -- {touche}")
    return manquements


def controler_la_conduite_apres_echec(texte: str, canon: str) -> list[str]:
    """Compare la conduite apres echec recopiee au canon, ligne a ligne."""
    if MARQUEUR_CONDUITE_DEBUT not in texte:
        return [f"conduite : marqueur absent -- {MARQUEUR_CONDUITE_DEBUT}"]
    if MARQUEUR_CONDUITE_FIN not in texte:
        return [f"conduite : marqueur absent -- {MARQUEUR_CONDUITE_FIN}"]
    if texte.find(MARQUEUR_CONDUITE_FIN) < texte.find(MARQUEUR_CONDUITE_DEBUT):
        return ["conduite : marqueurs inverses, la fin precede le debut"]

    attendu = normaliser(
        extraire_entre(canon, MARQUEUR_CONDUITE_DEBUT, MARQUEUR_CONDUITE_FIN, "conduite apres echec")
    )
    obtenu = normaliser(
        extraire_entre(texte, MARQUEUR_CONDUITE_DEBUT, MARQUEUR_CONDUITE_FIN, "conduite apres echec")
    )
    if obtenu == attendu:
        return []

    for rang, (ligne_attendue, ligne_obtenue) in enumerate(zip(attendu, obtenu), start=1):
        if ligne_attendue != ligne_obtenue:
            return [
                f"conduite : conduite apres echec alteree, ligne {rang} -- "
                f"attendu « {ligne_attendue} », obtenu « {ligne_obtenue} »"
            ]
    return [
        "conduite : conduite apres echec incomplete -- "
        f"{len(attendu)} lignes attendues, {len(obtenu)} recopiees"
    ]


def controler_les_notes(texte: str) -> list[str]:
    """
    Verifie les notes d'execution, ENTREE PAR ENTREE.

    Un comptage global se laisserait compenser : une entree portant deux statuts couvrirait une
    entree n'en portant aucun, et le total resterait juste. La mention « Aucun echec. » ne desactive
    rien : accompagnee d'une entree, elle la contredit, et c'est la contradiction qui est signalee.
    """
    titre = SECTIONS_DE_LA_CONDUITE[5]
    connues = positions(texte, SECTIONS_DE_LA_CONDUITE)
    if titre not in connues:
        return []
    notes = corps(texte, titre, connues)
    entrees = ENTREE.split(notes)[1:]
    mention = AUCUN_ECHEC in notes

    if mention and entrees:
        return [
            f"conduite : la mention « {AUCUN_ECHEC} » coexiste avec {len(entrees)} entree(s)"
        ]
    if not mention and not entrees:
        return [f"conduite : notes d'execution sans entree ni mention « {AUCUN_ECHEC} »"]

    manquements = []
    for entree in entrees:
        intitule = entree.splitlines()[0].strip() if entree.splitlines() else "(sans titre)"
        statuts = [valeur.strip().rstrip(".") for valeur in LIGNE_DE_STATUT.findall(entree)]
        if not statuts:
            manquements.append(f"conduite : entree sans statut -- {intitule}")
            continue
        if len(statuts) > 1:
            manquements.append(f"conduite : entree portant {len(statuts)} statuts -- {intitule}")
            continue
        if statuts[0].lower() not in STATUTS_ADMIS:
            manquements.append(
                f"conduite : statut hors des valeurs admises « {statuts[0]} » -- {intitule} "
                f"(admis : {', '.join(STATUTS_ADMIS)})"
            )
    return manquements


def controler_les_observations(texte: str) -> list[str]:
    """
    Verifie le dispositif et la presence d'au moins une observation.

    Les titres des observations sont libres -- ils nomment l'inconnue levee --, donc seuls le
    dispositif et leur nombre se controlent. Un document d'observations sans aucune observation est
    un faux vert : il atteste un dispositif qui n'a rien mesure.
    """
    manquements = controler_les_sections(
        "observations", texte, (TITRE_DU_DISPOSITIF,)
    )
    titres = TITRE_DE_SECTION.findall(texte)
    if titres and titres[0].strip() != TITRE_DU_DISPOSITIF:
        manquements.append(
            f"observations : « {TITRE_DU_DISPOSITIF} » n'est pas la premiere section"
        )
    if len(titres) < 2:
        manquements.append("observations : aucune observation, seulement le dispositif")
    return manquements


def controler_le_plan(texte: str, conduite: Path) -> list[str]:
    """
    Verifie le renvoi au document de conduite, la presence d'etapes, et la place du retrait.

    Le renvoi est controle parce que le plan ne porte ni le contrat de correction ni les notes : un
    renvoi faux laisserait l'executant sans conduite a tenir apres un echec, et rien ne le dirait.
    """
    manquements = []

    renvoi = None
    for ligne in texte.splitlines():
        if ligne.strip().startswith(RENVOI_DU_PLAN):
            renvoi = ligne.split(":", 1)[1].strip().strip("`\"'").strip()
            break
    if renvoi is None:
        manquements.append(f"plan : renvoi absent -- « {RENVOI_DU_PLAN} »")
    elif not resout_vers(renvoi, conduite):
        manquements.append(
            "plan : le renvoi ne resout pas vers le document de conduite. "
            f"Declare « {renvoi} », controle « {conduite.resolve()} »"
        )

    titres = [titre.strip() for titre in TITRE_DE_SECTION.findall(texte)]
    etapes = [titre for titre in titres if titre.startswith(PREFIXE_D_ETAPE)]
    if not etapes:
        manquements.append(f"plan : aucune section « {PREFIXE_D_ETAPE.strip()} <n> »")
    if TITRE_DU_RETRAIT not in titres:
        manquements.append(f"plan : section absente -- {TITRE_DU_RETRAIT}")
    elif etapes and titres.index(TITRE_DU_RETRAIT) < titres.index(etapes[-1]):
        manquements.append(
            f"plan : « {TITRE_DU_RETRAIT} » precede une etape ; il clot le plan"
        )
    return manquements


def controler_la_chaine(presents: dict[str, Path]) -> list[str]:
    """
    Verifie qu'aucun maillon amont ne manque.

    Une conduite peut s'arreter avant de produire un plan, et c'est legitime. Ce qui ne l'est pas,
    c'est un plan sans analyse ou une analyse sans observations : la phase aurait ete sautee, pas
    declaree.
    """
    manquements = []
    if "plan" in presents and "analyse" not in presents:
        manquements.append("chaine : un plan existe sans analyse")
    if "analyse" in presents and "observations" not in presents:
        manquements.append("chaine : une analyse existe sans observations")
    return manquements


def controler_les_blocs(document: str, texte: str, blocs: list[str]) -> list[str]:
    return [
        f"{document} : bloc du squelette reste a remplir -- {bloc}"
        for bloc in blocs
        if bloc in texte
    ]


def documents_compagnons(conduite: Path) -> dict[str, Path]:
    """Retourne les compagnons presents, deduits du nom du document de conduite."""
    nom = NOM_DE_LA_CONDUITE.match(conduite.name)
    if nom is None:
        raise ArgumentInvalide(
            f"le document de conduite doit se nommer conduite_<theme>.md, reçu « {conduite.name} »"
        )
    theme = nom.group("theme")
    presents = {}
    for compagnon in COMPAGNONS:
        chemin = conduite.parent / f"{compagnon}_{theme}.md"
        if chemin.is_file():
            presents[compagnon] = chemin
    return presents


def controler(conduite: Path, canon: str) -> list[str]:
    """Retourne la liste des manquements, vide si les documents sont conformes."""
    texte = lire(conduite)
    presents = documents_compagnons(conduite)
    blocs = blocs_des_squelettes(canon)

    manquements = [
        *controler_les_sections("conduite", texte, SECTIONS_DE_LA_CONDUITE),
        *controler_la_surface(texte, conduite),
        *controler_les_chemins_git(texte, conduite),
        *controler_la_conduite_apres_echec(texte, canon),
        *controler_les_notes(texte),
        *controler_les_blocs("conduite", texte, blocs),
        *controler_la_chaine(presents),
    ]

    for compagnon, chemin in presents.items():
        contenu = lire(chemin)
        if compagnon == "observations":
            manquements += controler_les_observations(contenu)
        elif compagnon == "analyse":
            manquements += controler_les_sections("analyse", contenu, SECTIONS_DE_L_ANALYSE)
        else:
            manquements += controler_le_plan(contenu, conduite)
        manquements += controler_les_blocs(compagnon, contenu, blocs)

    return manquements


def forcer_la_sortie_en_utf8() -> None:
    """
    Force les deux flux de sortie en UTF-8.

    Les manquements citent des titres de section accentues. Sans ce forcage, Python encode dans la
    page de code de la console -- cp1252 sous Windows -- et le titre ressort mutile dans un terminal
    qui lit de l'UTF-8. Un manquement illisible se lit comme un defaut du controle.
    """
    for flux in (sys.stdout, sys.stderr):
        reconfigurer = getattr(flux, "reconfigure", None)
        if reconfigurer is not None:
            reconfigurer(encoding="utf-8", errors="replace")


def main(arguments: list[str]) -> int:
    forcer_la_sortie_en_utf8()

    if len(arguments) != 1:
        print(
            "usage : python verifier_documents.py <chemin du document de conduite>",
            file=sys.stderr,
        )
        return 2

    conduite = Path(arguments[0])
    try:
        canon = lire(Path(__file__).resolve().parent / CANON)
        manquements = controler(conduite, canon)
    except CibleIntrouvable as absente:
        print(f"KO -- cible introuvable : {absente}", file=sys.stderr)
        return 3
    except ArgumentInvalide as invalide:
        print(f"KO -- appel invalide : {invalide}", file=sys.stderr)
        return 2
    except ControleImpossible as erreur:
        print(f"KO -- controle impossible : {erreur}", file=sys.stderr)
        return 3
    except (OSError, UnicodeDecodeError) as erreur:
        print(f"KO -- fichier illisible : {erreur}", file=sys.stderr)
        return 2

    if not manquements:
        print(f"OK -- documents conformes : {conduite}")
        return 0

    for manquement in manquements:
        print(f"  - {manquement}", file=sys.stderr)
    print(f"KO -- {len(manquements)} manquement(s) : {conduite}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
