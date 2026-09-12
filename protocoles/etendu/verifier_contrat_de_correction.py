"""
Controle du contrat de correction : le document declare porte-t-il la conduite a tenir apres un echec ?

Usage :
    python verifier_contrat_de_correction.py <chemin_du_document>

C'est le seul controle du protocole qui protege l'EXECUTANT plutot que le code livre, et le seul qui
soit entierement independant du projet et de sa technologie.

Le protocole impose de recopier integralement « La boucle de correction encadree » dans le dernier
document normatif produit avant d'agir -- le plan d'implementation quand la conduite en produit un,
le cadrage sinon -- parce que l'executant n'ouvre aucun autre document. Une prescription de recopie
ne se verifie pas par la lecture ; ce controle la transforme en barriere externe.

Il demeure obligatoire quelle que soit l'ampleur de la conduite. Une conduite partielle -- une
mesure, une observation -- ne livre rien mais agit quand meme, donc peut echouer : elle a le meme
besoin de ce contrat qu'une conduite complete.

Le document verifie remplit un ROLE, il n'a pas un type. Ce controle ne s'interesse pas a la nature
de l'artefact, seulement au role qu'il remplit.

Il echoue sur un marqueur absent, jamais sur un contenu supplementaire : il garantit une presence, il
ne contraint pas la redaction.

DECISION DE LANGUE, explicite et non subie : les marqueurs sont des litteraux francais accentues,
parce que le protocole est redige en francais. Une traduction du protocole traduit ces marqueurs dans
le meme mouvement, sans quoi le controle deviendrait inatteignable dans la langue cible. Ce script
est donc generique quant au projet, pas quant a la langue.

Codes de sortie :
    0 : aucun manquement
    1 : au moins un marqueur absent
    2 : usage incorrect
    3 : document introuvable ou illisible -- regle N10, un controle sans cible echoue
"""

from __future__ import annotations

import sys
from pathlib import Path


# Chaque entree associe un fragment a chercher dans le document portant le contrat et ce qu'il
# atteste. Les fragments sont courts et semantiquement porteurs, pour resister a une reformulation
# mineure sans laisser passer une section absente.
MARQUEURS_DU_CONTRAT_DE_CORRECTION = (
    ("Conduite à tenir quand une validation échoue", "la section elle-meme"),
    ("exécutée comme écrite", "distinction entre action mal executee et echec reel"),
    ("Notes d'exécution", "emplacement de la fiche a ecrire avant correction"),
    ("Surface d'écriture autorisée", "surfaces autorisees par classe de KO"),
    ("ne jamais modifier une validation", "interdit qui prime sur les autres"),
    ("Deux tentatives", "plafond de tentatives par symptome"),
    ("arrêt immédiat", "liste des cas d'arret"),
    ("Un arrêt n'est pas un échec", "la phrase sans laquelle un executant s'obstine"),
)


def marqueurs_absents(texte: str) -> list[tuple[str, str]]:
    """Retourne les marqueurs que le document ne porte pas, avec ce que chacun atteste."""
    return [(fragment, atteste)
            for fragment, atteste in MARQUEURS_DU_CONTRAT_DE_CORRECTION
            if fragment not in texte]


def controler(chemin: Path) -> int:
    """Lit le document et retourne le code de sortie du controle."""
    try:
        texte = chemin.read_text(encoding="utf-8-sig")
    except OSError as erreur:
        print(f"Erreur -- document introuvable ou illisible : {chemin.as_posix()} ({erreur})",
              file=sys.stderr)
        print("Regle N10 : un controle sans cible echoue, il ne passe pas.", file=sys.stderr)
        return 3

    absents = marqueurs_absents(texte)
    if not absents:
        print("OK -- le contrat de correction est present et complet.")
        return 0

    for fragment, atteste in absents:
        print(f"KO | contrat de correction incomplet | {chemin.as_posix()} | "
              f"marqueur absent : {atteste} (\"{fragment}\")", file=sys.stderr)
    print(f"KO -- {len(absents)} marqueur(s) absent(s).", file=sys.stderr)
    return 1


def main() -> int:
    """Point d'entree."""
    if len(sys.argv) != 2:
        print("Usage : python verifier_contrat_de_correction.py <chemin_du_document>",
              file=sys.stderr)
        return 2
    return controler(Path(sys.argv[1]))


if __name__ == "__main__":
    raise SystemExit(main())
