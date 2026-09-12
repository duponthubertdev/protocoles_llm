"""Eprouve le parseur de fiches sur les deux etats : sous-section legitime contre fiche reelle."""
import subprocess
import sys

import test_porte as base

FICHE_CLOSE = [
    "### Étape 1 -- un échec",
    "",
    "**Statut :** CLOSE",
    "",
    "**Symptôme :** quelque chose.",
    "",
]

FICHE_OUVERTE = [
    "### Étape 2 -- un autre échec",
    "",
    "**Statut :** OUVERTE",
    "",
    "**Symptôme :** autre chose.",
    "",
]

FICHE_SANS_STATUT = [
    "### Étape 3 -- un troisième échec",
    "",
    "**Symptôme :** encore autre chose.",
    "",
    "**Classe :** attendu faux",
    "",
]

SOUS_SECTION = [
    "### Contexte de la reprise",
    "",
    "Une sous-section legitime : elle ne porte aucun champ du format de fiche.",
    "",
    "Elle explique le contexte, et rien de plus.",
    "",
]


def contrat_avec(blocs):
    lignes = list(base.CONTRAT_BASE) + ["## Notes d'exécution", ""]
    for bloc in blocs:
        lignes += bloc
    return "\n".join(lignes)


def essai(nom, blocs, attendu):
    base.construire()
    (base.DEPOT / "chantier" / "plan.md").write_text(contrat_avec(blocs), encoding="utf-8")
    base.git("add", "chantier/plan.md")
    base.git("commit", "-q", "-m", "notes")
    resultat = subprocess.run([sys.executable, base.PORTE, base.manifeste()],
                              capture_output=True, text=True)
    conforme = resultat.returncode == attendu
    print(("OK  " if conforme else "ECHEC DU TEST"),
          f"{nom:56} attendu={attendu} constate={resultat.returncode}")
    if not conforme:
        print(resultat.stdout, resultat.stderr)
    return conforme


def main() -> int:
    r = []
    r.append(essai("sous-section seule, aucune fiche -> 0", [SOUS_SECTION], 0))
    r.append(essai("sous-section + fiche close -> 0", [SOUS_SECTION, FICHE_CLOSE], 0))
    r.append(essai("sous-section + fiche ouverte -> 1", [SOUS_SECTION, FICHE_OUVERTE], 1))
    r.append(essai("sous-section + fiche sans statut -> 1", [SOUS_SECTION, FICHE_SANS_STATUT], 1))
    r.append(essai("fiche sans statut seule -> 1 (non regression)", [FICHE_SANS_STATUT], 1))
    r.append(essai("deux sous-sections, aucune fiche -> 0", [SOUS_SECTION, SOUS_SECTION], 0))
    print(f"\n{sum(r)}/{len(r)} tests conformes")
    return 0 if sum(r) == len(r) else 1


if __name__ == "__main__":
    raise SystemExit(main())
