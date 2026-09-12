"""
Suite du verificateur de documents.

Elle exerce le cas conforme et les etats interdits. Chaque cas est une mutation des quatre
documents de `tests/donnees/` : ceux-ci sont donc a la fois le controle positif et la matiere des controles
negatifs, ce qui interdit qu'ils derivent des squelettes sans que la suite le voie.

POURQUOI CES TESTS EXISTENT. Un controle qui n'a ete essaye que sur un cas conforme ne prouve rien :
il prouve que ce cas passe, pas que les etats interdits echouent. Un verificateur qui retournerait 0
sur tout serait vert sur les documents de reference, et ne protegerait de rien.

POURQUOI DEUX LIGNES SONT REECRITES. Le verificateur exige que la premiere entree de la surface et le
renvoi du plan resolvent vers le document de conduite controle. Les documents de `tests/donnees/` portent
des chemins fictifs, pour rester lisibles : y mettre leurs vrais chemins lierait le controle positif
a l'emplacement exact du paquet, et le casserait au premier rangement. La suite les recopie dans un
dossier temporaire et reecrit ces deux lignes vers les copies. Ce sont les seules qu'elle modifie sur
le cas conforme.

Lancer :

    python tests\\lancer_les_tests.py

Code de sortie 0 si tous les cas sont conformes a leur attendu, 1 sinon.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
VERIFICATEUR = RACINE / "verifier_documents.py"
DONNEES = RACINE / "tests" / "donnees"

CONDUITE = "conduite_decompte.md"
OBSERVATIONS = "observations_decompte.md"
ANALYSE = "analyse_decompte.md"
PLAN = "plan_decompte.md"
TOUS = (CONDUITE, OBSERVATIONS, ANALYSE, PLAN)

RACINE_FICTIVE = r"C:\Users\hdupo\git\projet-fictif"
COMMIT_FICTIF = "4c19ab7"
MARQUEUR_FIN = "<!-- CONDUITE APRES ECHEC : FIN -->"
TITRE_SURFACE = "## 1. Surface d'écriture"
TITRE_NOTES = "## 6. Notes d'exécution"
TITRE_CLOTURE = "## 7. Clôture"
TITRE_RETRAIT = "## Retrait des artefacts temporaires"


def lancer(*arguments: str, depuis: Path | None = None) -> int:
    """Retourne le code de sortie du verificateur, sa sortie etant sans objet ici."""
    script = str((depuis / "verifier_documents.py") if depuis else VERIFICATEUR)
    acheve = subprocess.run(
        [sys.executable, script, *arguments],
        capture_output=True,
        cwd=str(depuis or RACINE),
    )
    return acheve.returncode


def git(dossier: Path, *arguments: str) -> str:
    """Execute Git dans le depot temporaire et echoue avec son diagnostic."""
    acheve = subprocess.run(
        ["git", "-C", str(dossier), *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if acheve.returncode != 0:
        raise AssertionError(
            f"git {' '.join(arguments)} a echoue : {acheve.stderr.strip()}"
        )
    return acheve.stdout.strip()


def initialiser_depot(dossier: Path, fichier_initial: tuple[str, str] | None = None) -> str:
    """Cree un depot autonome et retourne son commit de depart."""
    git(dossier, "init")
    git(dossier, "config", "user.name", "Protocole standard")
    git(dossier, "config", "user.email", "protocole-standard@example.invalid")
    initial = dossier / (fichier_initial[0] if fichier_initial else ".depart")
    initial.parent.mkdir(parents=True, exist_ok=True)
    initial.write_text(fichier_initial[1] if fichier_initial else "depart\n", encoding="utf-8")
    git(dossier, "add", "--", str(initial.relative_to(dossier)))
    git(dossier, "commit", "-m", "depart")
    return git(dossier, "rev-parse", "HEAD")


def remplacer(source: str, ancien: str, nouveau: str) -> str:
    """Remplace un fragment, en echouant bruyamment s'il a disparu des documents de reference."""
    if ancien not in source:
        raise AssertionError(f"fragment introuvable dans les documents de reference : {ancien!r}")
    return source.replace(ancien, nouveau, 1)


def muter(documents: dict[str, str], nom: str, ancien: str, nouveau: str) -> dict[str, str]:
    """Retourne les documents avec un fragment remplace dans l'un d'eux."""
    mutes = dict(documents)
    mutes[nom] = remplacer(mutes[nom], ancien, nouveau)
    return mutes


def sans(documents: dict[str, str], nom: str) -> dict[str, str]:
    """Retourne les documents prives de l'un d'eux."""
    mutes = dict(documents)
    del mutes[nom]
    return mutes


def premiere_puce(source: str, titre: str) -> str:
    """Retourne la premiere puce d'une section, pour pouvoir la remplacer ou la retirer."""
    lignes = source.split("\n")
    debut = lignes.index(titre)
    for rang in range(debut, len(lignes)):
        if lignes[rang].startswith("- "):
            return lignes[rang]
    raise AssertionError(f"aucune puce sous {titre}")


def permuter_notes_et_cloture(source: str) -> str:
    """Retourne la conduite avec les notes d'execution placees APRES la cloture."""
    debut = source.index(f"\n{TITRE_NOTES}")
    milieu = source.index(f"\n{TITRE_CLOTURE}")
    return source[:debut] + source[milieu:] + source[debut:milieu]


def vider_la_cloture(source: str) -> str:
    """Retourne la conduite dont la derniere section ne porte plus que son titre."""
    return source[:source.index(f"\n{TITRE_CLOTURE}")] + f"\n{TITRE_CLOTURE}\n\n"


def notes_sans_entree_ni_mention(source: str) -> str:
    """Retourne la conduite dont les notes portent de la prose, mais ni entree ni mention."""
    debut = source.index(f"\n{TITRE_NOTES}")
    fin = source.index(f"\n{TITRE_CLOTURE}")
    return (
        source[:debut]
        + f"\n{TITRE_NOTES}\n\nLe détail figure dans le journal d'exécution.\n"
        + source[fin:]
    )


def permuter_sections_de_l_analyse(source: str) -> str:
    """Retourne l'analyse avec « Divergences » placee avant « Decisions »."""
    a = source.index("\n## Décisions")
    b = source.index("\n## Divergences avec le cadrage")
    c = source.index("\n## Fichiers touchés")
    return source[:a] + source[b:c] + source[a:b] + source[c:]


def remonter_le_retrait(source: str) -> str:
    """Retourne le plan dont le retrait des artefacts precede la derniere etape."""
    debut = source.index(f"\n{TITRE_RETRAIT}")
    retrait = source[debut:].rstrip() + "\n"
    reste = source[:debut]
    derniere = reste.rindex("\n## Étape ")
    return reste[:derniere] + retrait + reste[derniere:]


def cas(reference: dict[str, str], dossier: Path) -> list[tuple[str, dict[str, str], int]]:
    """Retourne les cas : intitule, contenu des documents, code de sortie attendu."""
    conduite = reference[CONDUITE]
    puce = premiere_puce(conduite, TITRE_SURFACE)
    ailleurs = dossier / "ailleurs" / CONDUITE
    return [
        ("documents conformes", reference, 0),

        ("conduite : section absente",
         muter(reference, CONDUITE, "## 3. Cartographie", "## 3. Carto"), 1),
        ("conduite : sections dans le désordre",
         {**reference, CONDUITE: permuter_notes_et_cloture(conduite)}, 1),
        ("conduite : section vide",
         {**reference, CONDUITE: vider_la_cloture(conduite)}, 1),
        ("surface : première entrée absente",
         muter(reference, CONDUITE, puce + "\n", ""), 1),
        ("surface : première entrée désignant un homonyme ailleurs",
         muter(reference, CONDUITE, puce, f"- `{ailleurs}`"), 1),
        ("surface : première entrée en chemin relatif",
         muter(reference, CONDUITE, puce, f"- `{CONDUITE}`"), 1),
        ("conduite après échec : tronquée",
         muter(reference, CONDUITE,
               "4. Deux tentatives au plus sur le même échec. À la troisième, s'arrêter et rendre\n"
               "   la main, en laissant l'état tel quel.\n", ""), 1),
        ("conduite après échec : altérée en conservant sa structure",
         muter(reference, CONDUITE, "4. Deux tentatives au plus", "4. Trois tentatives au plus"), 1),
        ("conduite après échec : adoucie sur la correction d'un attendu",
         muter(reference, CONDUITE,
               "3. Un attendu ne se corrige que contre une preuve antérieure à l'échec, jamais",
               "3. Un attendu peut se corriger après un échec, jamais"), 1),
        ("conduite après échec : marqueur de fin absent",
         muter(reference, CONDUITE, MARQUEUR_FIN, ""), 1),
        ("conduite : bloc du squelette résiduel",
         muter(reference, CONDUITE, "-> vert, artefact : `C:", "-> <verdict>, artefact : `C:"), 1),
        ("notes : statut absent",
         muter(reference, CONDUITE, "- Statut : clos", ""), 1),
        ("notes : statut hors des valeurs admises",
         muter(reference, CONDUITE, "- Statut : clos", "- Statut : en cours"), 1),
        ("notes : statut en double",
         muter(reference, CONDUITE, "- Statut : clos", "- Statut : clos\n- Statut : clos"), 1),
        ("notes : « Aucun échec. » coexistant avec une entrée",
         muter(reference, CONDUITE, f"\n{TITRE_NOTES}\n", f"\n{TITRE_NOTES}\n\nAucun échec.\n"), 1),
        ("notes : ni entrée ni mention",
         {**reference, CONDUITE: notes_sans_entree_ni_mention(conduite)}, 1),

        ("observations : dispositif absent",
         muter(reference, OBSERVATIONS, "## Dispositif", "## Comment on a mesuré"), 1),
        ("observations : dispositif seul, aucune observation",
         {**reference, OBSERVATIONS: reference[OBSERVATIONS].split("\n## Le décompte")[0]}, 1),
        ("observations : bloc du squelette résiduel",
         muter(reference, OBSERVATIONS, "- Retrait prévu : étape 3 du plan",
               "- Retrait prévu : <l'étape du plan qui la supprime, ou : elle reste livrée>"), 1),

        ("analyse : section absente",
         muter(reference, ANALYSE, "## Fichiers touchés", "## Fichiers"), 1),
        ("analyse : sections dans le désordre",
         {**reference, ANALYSE: permuter_sections_de_l_analyse(reference[ANALYSE])}, 1),
        ("analyse : section vide",
         muter(reference, ANALYSE, "## Divergences avec le cadrage\n\nAucune.\n",
               "## Divergences avec le cadrage\n\n"), 1),

        ("plan : renvoi à la conduite absent",
         muter(reference, PLAN, "Contrat de correction et notes d'exécution :", "Voir aussi :"), 1),
        ("plan : renvoi pointant ailleurs",
         muter(reference, PLAN, str(dossier / CONDUITE), str(ailleurs)), 1),
        ("plan : aucune étape",
         {**reference, PLAN: reference[PLAN].replace("\n## Étape ", "\n### Étape ")}, 1),
        ("plan : le retrait précède la dernière étape",
         {**reference, PLAN: remonter_le_retrait(reference[PLAN])}, 1),

        ("chaîne : un plan sans analyse", sans(reference, ANALYSE), 1),
        ("chaîne : une analyse sans observations", sans(reference, OBSERVATIONS), 1),
    ]


def ecrire(documents: dict[str, str], dossier: Path) -> None:
    """Ecrit les documents du cas, et retire ceux que la mutation a supprimes."""
    for nom in TOUS:
        chemin = dossier / nom
        if nom in documents:
            chemin.write_text(documents[nom], encoding="utf-8")
        elif chemin.exists():
            chemin.unlink()


def adapter(dossier: Path, depart: str) -> dict[str, str]:
    """Recopie les documents de reference en les rattachant au depot temporaire."""
    documents = {}
    for nom in TOUS:
        texte = (DONNEES / nom).read_text(encoding="utf-8")
        texte = texte.replace(f"{RACINE_FICTIVE}\\notes", str(dossier))
        texte = texte.replace(RACINE_FICTIVE, str(dossier))
        if nom == CONDUITE:
            texte = remplacer(texte, COMMIT_FICTIF, depart)
        documents[nom] = texte
    return documents


def verifier_cas_git(
    intitule: str,
    attendu: int,
    preparer,
    fichier_initial: tuple[str, str] | None = None,
) -> int:
    """Construit un depot neuf, applique un cas Git et retourne 1 si son verdict diverge."""
    with tempfile.TemporaryDirectory() as temporaire:
        dossier = Path(temporaire)
        depart = initialiser_depot(dossier, fichier_initial)
        reference = adapter(dossier, depart)
        ecrire(reference, dossier)
        preparer(dossier, depart, reference)
        obtenu = lancer(str(dossier / CONDUITE))
    print(f"  [{'ok' if obtenu == attendu else 'ECHEC'}] {intitule} : attendu {attendu}, obtenu {obtenu}")
    return obtenu != attendu


def tester_la_surface_git() -> int:
    """Exerce les chemins suivis, non suivis, toleres et disparus du diff final."""
    echecs = 0

    def ne_rien_faire(dossier: Path, depart: str, reference: dict[str, str]) -> None:
        pass

    def creer_hors_surface(dossier: Path, depart: str, reference: dict[str, str]) -> None:
        (dossier / "hors_surface.txt").write_text("hors surface\n", encoding="utf-8")

    def committer_hors_surface(dossier: Path, depart: str, reference: dict[str, str]) -> None:
        creer_hors_surface(dossier, depart, reference)
        git(dossier, "add", "--", "hors_surface.txt")
        git(dossier, "commit", "-m", "hors surface")

    def creer_sortie_technique(dossier: Path, depart: str, reference: dict[str, str]) -> None:
        sortie = dossier / "sortie" / "validation" / "temporaire.txt"
        sortie.parent.mkdir(parents=True, exist_ok=True)
        sortie.write_text("sortie attendue\n", encoding="utf-8")

    def invalider_commit(dossier: Path, depart: str, reference: dict[str, str]) -> None:
        document = dossier / CONDUITE
        document.write_text(
            remplacer(document.read_text(encoding="utf-8"), depart, "commit-introuvable"),
            encoding="utf-8",
        )

    def sorties_sans_backticks(dossier: Path, depart: str, reference: dict[str, str]) -> None:
        document = dossier / CONDUITE
        texte = document.read_text(encoding="utf-8")
        ligne = next(
            ligne
            for ligne in texte.splitlines()
            if ligne.startswith("- Fichiers qu'une exécution modifie")
        )
        document.write_text(
            remplacer(texte, ligne, ligne.replace("`", "")),
            encoding="utf-8",
        )

    def modifier_puis_restaurer(dossier: Path, depart: str, reference: dict[str, str]) -> None:
        chemin = dossier / "hors_surface.txt"
        chemin.write_text("modifie\n", encoding="utf-8")
        git(dossier, "add", "--", "hors_surface.txt")
        git(dossier, "commit", "-m", "modification hors surface")
        chemin.write_text("origine\n", encoding="utf-8")
        git(dossier, "add", "--", "hors_surface.txt")
        git(dossier, "commit", "-m", "restauration hors surface")

    echecs += verifier_cas_git("surface Git : cas conforme", 0, ne_rien_faire)
    echecs += verifier_cas_git("surface Git : fichier non suivi hors surface", 1, creer_hors_surface)
    echecs += verifier_cas_git("surface Git : fichier commite hors surface", 1, committer_hors_surface)
    echecs += verifier_cas_git("surface Git : sortie technique toleree", 0, creer_sortie_technique)
    echecs += verifier_cas_git("surface Git : commit de depart invalide", 1, invalider_commit)
    echecs += verifier_cas_git("surface Git : sortie technique sans backticks", 1, sorties_sans_backticks)
    echecs += verifier_cas_git(
        "surface Git : modification hors surface restauree ensuite",
        1,
        modifier_puis_restaurer,
        ("hors_surface.txt", "origine\n"),
    )
    return echecs


def executer() -> int:
    echecs = 0

    with tempfile.TemporaryDirectory() as temporaire:
        dossier = Path(temporaire)
        depart = initialiser_depot(dossier)
        reference = adapter(dossier, depart)
        conduite = dossier / CONDUITE

        for intitule, documents, attendu in cas(reference, dossier):
            ecrire(documents, dossier)
            obtenu = lancer(str(conduite))
            if obtenu != attendu:
                echecs += 1
            verdict = "ok" if obtenu == attendu else "ECHEC"
            print(f"  [{verdict}] {intitule} : attendu {attendu}, obtenu {obtenu}")

        ecrire(reference, dossier)

        # Le document de conduite est introuvable : le controle doit le nommer, jamais passer au vert.
        obtenu = lancer(str(dossier / "conduite_neexistepas.md"))
        echecs += obtenu != 3
        print(f"  [{'ok' if obtenu == 3 else 'ECHEC'}] conduite introuvable : attendu 3, obtenu {obtenu}")

        # Le nom ne permet pas de deduire les compagnons : l'appel est invalide, pas fautif.
        mal_nomme = dossier / "notes_decompte.md"
        mal_nomme.write_text(reference[CONDUITE], encoding="utf-8")
        obtenu = lancer(str(mal_nomme))
        echecs += obtenu != 2
        print(f"  [{'ok' if obtenu == 2 else 'ECHEC'}] nom de document invalide : attendu 2, obtenu {obtenu}")
        mal_nomme.unlink()

        # Le canon est introuvable : le verificateur est isole de `protocole.md`. Sans ce cas,
        # rien ne distinguerait un canon absent d'un canon vide, et un bloc vide serait compare a
        # rien -- donc conforme.
        isole = dossier / "isole"
        isole.mkdir()
        shutil.copy(VERIFICATEUR, isole / "verifier_documents.py")
        obtenu = lancer(str(conduite), depuis=isole)
        echecs += obtenu != 3
        print(f"  [{'ok' if obtenu == 3 else 'ECHEC'}] canon introuvable : attendu 3, obtenu {obtenu}")

        # Aucun argument : l'appel est invalide, ce qui n'est pas un manquement des documents.
        obtenu = lancer()
        echecs += obtenu != 2
        print(f"  [{'ok' if obtenu == 2 else 'ECHEC'}] sans argument : attendu 2, obtenu {obtenu}")

    echecs += tester_la_surface_git()
    return echecs


def main() -> int:
    for flux in (sys.stdout, sys.stderr):
        reconfigurer = getattr(flux, "reconfigure", None)
        if reconfigurer is not None:
            reconfigurer(encoding="utf-8", errors="replace")

    print("Suite du vérificateur de documents")
    echecs = executer()
    if echecs:
        print(f"\nKO -- {echecs} cas non conforme(s) à leur attendu.", file=sys.stderr)
        return 1
    print("\nOK -- tous les cas sont conformes à leur attendu.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
