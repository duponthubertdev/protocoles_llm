"""
Lance toutes les verifications du paquet, et retourne un code de sortie unique.

Usage :
    python tests/lancer_les_tests.py

C'est la commande a passer apres tout changement du paquet. Elle enchaine, dans cet ordre :

1. la compilation de tous les scripts ;
2. les vingt et un cas des deux suites -- la porte de publication et le parseur de fiches ;
3. le controle positif du contrat de correction, sur un document fictif local ;
4. l'extraction du bloc canonique, verifiee sur ses huit marqueurs et son absence de code interne.

Le quatrieme controle est celui qui garantit la propriete la plus facile a casser sans s'en
apercevoir : un simple retour a la ligne coupant un marqueur en deux suffit, et c'est deja arrive.

Codes de sortie :
    0 : tout est conforme
    1 : au moins une verification a echoue
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

PAQUET = Path(__file__).resolve().parent.parent
PROTOCOLE = PAQUET / "protocole.md"

MARQUEUR_DEBUT = "<!-- CONTRAT DE CORRECTION : DEBUT -->"
MARQUEUR_FIN = "<!-- CONTRAT DE CORRECTION : FIN -->"

# Document fictif local servant de controle positif au contrat de correction.
# Son absence fait echouer le controle.
PLAN_DE_REFERENCE = PAQUET / "tests" / "donnees" / "plan_fictif.md"


def lancer(titre: str, arguments: list[str]) -> bool:
    """Execute une commande et rapporte son verdict."""
    resultat = subprocess.run([sys.executable, *arguments], cwd=PAQUET,
                              capture_output=True, text=True, encoding="utf-8", errors="replace")
    conforme = resultat.returncode == 0
    print(f"{'OK  ' if conforme else 'KO  '} {titre}")
    if not conforme:
        print((resultat.stdout or "") + (resultat.stderr or ""))
    return conforme


def extraire_le_bloc() -> str | None:
    """Retourne le contenu du bloc canonique, ou None s'il n'est pas delimite."""
    texte = PROTOCOLE.read_text(encoding="utf-8")
    if MARQUEUR_DEBUT not in texte or MARQUEUR_FIN not in texte:
        return None
    debut = texte.index(MARQUEUR_DEBUT) + len(MARQUEUR_DEBUT)
    return texte[debut:texte.index(MARQUEUR_FIN)]


def controler_le_bloc() -> bool:
    """
    Verifie que le bloc canonique est delimite, generique et complet.

    Ces trois proprietes sont ce qui rend la recopie mecanique. Les perdre ne casse rien
    visiblement : le protocole reste lisible, et seule une conduite ulterieure en paierait le prix.
    """
    bloc = extraire_le_bloc()
    if bloc is None:
        print("KO   bloc canonique : marqueurs de delimitation absents")
        return False

    manquements = []

    marqueurs = ("Conduite à tenir quand une validation échoue", "exécutée comme écrite",
                 "Notes d'exécution", "Surface d'écriture autorisée",
                 "ne jamais modifier une validation", "Deux tentatives", "arrêt immédiat",
                 "Un arrêt n'est pas un échec")
    absents = [m for m in marqueurs if m not in bloc]
    if absents:
        manquements.append(f"marqueurs absents du bloc : {absents}")

    codes = sorted(set(re.findall(r"\b[ENSP]\d+\b", bloc)))
    if codes:
        manquements.append(f"codes internes dans le bloc, illisibles pour un executant froid : {codes}")

    for terme in ("cadrage", "plan d'impl"):
        if terme in bloc.lower():
            manquements.append(f"le bloc nomme « {terme} » : il doit rester generique")

    for attendu, quoi in (("régime d'autorisation du dépôt est absent", "l'arret sur l'autorisation"),
                          ("Reprendre à l'étape minimale suffisante", "la procedure de reprise")):
        if attendu not in bloc:
            manquements.append(f"{quoi} a disparu du bloc")

    if manquements:
        print("KO   bloc canonique")
        for m in manquements:
            print(f"       {m}")
        return False
    print(f"OK   bloc canonique : {len(bloc.splitlines())} lignes, generique et complet")
    return True


def main() -> int:
    """Point d'entree."""
    resultats = []

    scripts = sorted(str(c.relative_to(PAQUET)) for c in PAQUET.glob("*.py"))
    resultats.append(lancer("compilation des scripts", ["-m", "py_compile", *scripts]))

    resultats.append(lancer("porte de publication, quinze cas", ["tests/test_porte.py"]))
    resultats.append(lancer("parseur de fiches, six cas", ["tests/test_sous_sections.py"]))

    if PLAN_DE_REFERENCE.exists():
        resultats.append(lancer("contrat de correction, controle positif",
                                ["verifier_contrat_de_correction.py", str(PLAN_DE_REFERENCE)]))
    else:
        print(f"KO   contrat de correction : plan de reference introuvable\n"
              f"       {PLAN_DE_REFERENCE.as_posix()}\n"
              f"       Regle N10 : un controle sans cible echoue, il ne passe pas.")
        resultats.append(False)

    resultats.append(controler_le_bloc())

    reussis = sum(1 for r in resultats if r)
    print(f"\n{reussis}/{len(resultats)} verifications conformes")
    return 0 if reussis == len(resultats) else 1


if __name__ == "__main__":
    raise SystemExit(main())
