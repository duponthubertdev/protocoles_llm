"""
Eprouve la porte de publication sur les deux etats de chacun de ses discriminants.

Usage : python tests/test_porte.py

Construit un depot git jetable dans le repertoire temporaire du systeme, et rejoue la
porte sur quinze etats. Un discriminant se prouve sur les deux etats : chaque cas qui
doit echouer a son pendant qui doit passer.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

PAQUET = pathlib.Path(__file__).resolve().parent.parent
SCRATCH = pathlib.Path(tempfile.gettempdir()) / "protocole_etendu_tests"
SCRATCH.mkdir(exist_ok=True)
DEPOT = SCRATCH / "depot_porte"
PORTE = str(PAQUET / "verifier_porte_de_publication.py")

CONTRAT_BASE = [
    "# Plan",
    "",
    "## Conduite à tenir quand une validation échoue",
    "",
    "L'action a été exécutée comme écrite et la validation échoue quand même.",
    "**Surface d'écriture autorisée :** aucune",
    "Interdit qui prime : ne jamais modifier une validation pour la faire passer.",
    "Deux tentatives sur le même symptôme.",
    "Cas d'arrêt immédiat : la liste.",
    "Un arrêt n'est pas un échec de l'exécutant.",
    "",
]


def git(*arguments):
    subprocess.run(["git", *arguments], cwd=DEPOT, check=True,
                   capture_output=True, text=True)


def contrat(fiches):
    lignes = list(CONTRAT_BASE) + ["## Notes d'exécution", ""]
    for titre, statut in fiches:
        lignes += [f"### {titre}", ""]
        if statut:
            lignes += [f"**Statut :** {statut}", ""]
        lignes += ["**Symptôme :** quelque chose.", ""]
    return "\n".join(lignes)


def construire(fiches=(("Étape 1 -- un échec", "CLOSE"),)):
    """Reconstruit un depot propre, sur une branche de sujet conforme, tout commite."""
    if DEPOT.exists():
        shutil.rmtree(DEPOT, ignore_errors=True)
    (DEPOT / "chantier").mkdir(parents=True)
    (DEPOT / "src").mkdir()
    (DEPOT / "parametrage").mkdir()
    git("init", "-q")
    git("config", "user.email", "test@example.invalid")
    git("config", "user.name", "test")
    (DEPOT / "chantier" / "plan.md").write_text(contrat(fiches), encoding="utf-8")
    (DEPOT / "src" / "livrable.txt").write_text("livre\n", encoding="utf-8")
    (DEPOT / "parametrage" / "selection.txt").write_text("chaine_a\n", encoding="utf-8")
    (DEPOT / "hors_perimetre.txt").write_text("autre chantier\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-q", "-m", "etat initial")
    git("branch", "-M", "feat/42-un-sujet-de-test")


def manifeste(**surcharges):
    base = {
        "racine_depot": DEPOT.as_posix(),
        "contrat_de_correction": "chantier/plan.md",
        "branche_du_sujet": "feat/42-un-sujet-de-test",
        "perimetre": ["src/livrable.txt"],
    }
    base.update(surcharges)
    chemin = SCRATCH / "manifeste_porte.json"
    chemin.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
    return str(chemin)


def essai(nom, chemin_manifeste, attendu):
    resultat = subprocess.run([sys.executable, PORTE, chemin_manifeste],
                              capture_output=True, text=True)
    conforme = resultat.returncode == attendu
    print(("OK  " if conforme else "ECHEC DU TEST"),
          f"{nom:52} attendu={attendu} constate={resultat.returncode}")
    if not conforme:
        print(resultat.stdout, resultat.stderr)
    return conforme


def main() -> int:
    total = []

    construire()
    total.append(essai("etat propre, fiche CLOSE -> 0", manifeste(), 0))

    construire(fiches=(("Étape 1 -- un échec", "OUVERTE"),))
    total.append(essai("fiche OUVERTE -> 1", manifeste(), 1))

    construire(fiches=(("Étape 1 -- un échec", None),))
    total.append(essai("fiche sans statut -> 1", manifeste(), 1))

    construire(fiches=(("Étape 1", "CLOSE"), ("Étape 2", "OUVERTE")))
    total.append(essai("une fiche close, une ouverte -> 1", manifeste(), 1))

    construire()
    (DEPOT / "chantier" / "plan.md").write_text(
        "\n".join(CONTRAT_BASE), encoding="utf-8")
    git("add", "chantier/plan.md")
    git("commit", "-q", "-m", "sans notes")
    total.append(essai("section des notes absente -> 1", manifeste(), 1))

    construire()
    git("branch", "-M", "main")
    total.append(essai("branche principale -> 1",
                       manifeste(branche_du_sujet="main"), 1))

    construire()
    git("branch", "-M", "un-nom-libre")
    total.append(essai("nom de branche hors convention -> 1",
                       manifeste(branche_du_sujet="un-nom-libre"), 1))

    construire()
    total.append(essai("branche differente de celle declaree -> 1",
                       manifeste(branche_du_sujet="feat/43-autre-sujet"), 1))

    construire()
    total.append(essai("branche_du_sujet absente du manifeste -> 2",
                       manifeste_sans_branche(), 2))

    construire()
    (DEPOT / "src" / "livrable.txt").write_text("modifie\n", encoding="utf-8")
    total.append(essai("fichier du perimetre non commite -> 1", manifeste(), 1))

    construire()
    (DEPOT / "src" / "neuf.txt").write_text("neuf\n", encoding="utf-8")
    total.append(essai("fichier non suivi dans le perimetre -> 1",
                       manifeste(perimetre=["src"]), 1))

    construire()
    (DEPOT / "ailleurs_non_suivi.txt").write_text("autre chantier\n", encoding="utf-8")
    total.append(essai("fichier non suivi HORS perimetre -> 0 (ignore)", manifeste(), 0))

    construire()
    (DEPOT / "hors_perimetre.txt").write_text("modifie\n", encoding="utf-8")
    total.append(essai("fichier suivi modifie hors perimetre -> 1", manifeste(), 1))

    construire()
    (DEPOT / "chantier" / "faits.md").write_text("observation\n", encoding="utf-8")
    total.append(essai("artefact de chantier non commite -> 1", manifeste(), 1))

    construire()
    racine_hors_depot = SCRATCH / "pas_un_depot"
    racine_hors_depot.mkdir(exist_ok=True)
    total.append(essai("racine sans depot git -> 4 (indecidable)",
                       manifeste(racine_depot=racine_hors_depot.as_posix()), 4))

    reussis = sum(1 for essai_ok in total if essai_ok)
    print(f"\n{reussis}/{len(total)} tests conformes")
    return 0 if reussis == len(total) else 1


def manifeste_sans_branche():
    base = {
        "racine_depot": DEPOT.as_posix(),
        "contrat_de_correction": "chantier/plan.md",
        "perimetre": ["src/livrable.txt"],
    }
    chemin = SCRATCH / "manifeste_porte.json"
    chemin.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
    return str(chemin)


if __name__ == "__main__":
    raise SystemExit(main())
