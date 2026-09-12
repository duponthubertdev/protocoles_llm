"""
Hygiene des chemins d'un manifeste de conduite.

Deux façons de s'en servir, et une seule logique.

1. **Comme bibliotheque**, depuis le controle statique d'un projet -- cas normal, parce que seul ce
   script sait quelles cles portent des chemins :

       from verifier_chemins_declares import controler_les_chemins_declares
       controler_les_chemins_declares(racine, [*manifeste["vues"], manifeste["dossier_captures"]])

2. **En ligne de commande**, pour un manifeste qui declare ses chemins a plat sous `perimetre` :

       python verifier_chemins_declares.py <chemin_du_manifeste>

POURQUOI CE CONTROLE EXISTE. Un chemin absolu, ou remontant par `..`, reste lisible par les controles
de contenu : `Path` le resout sans broncher, et le fichier est bien inspecte. Mais git ne produit que
des chemins relatifs a la racine du depot. Le perimetre ne correspondrait alors a rien de ce que git
annonce, et un fichier declare mais non commite passerait inapercu a la porte de publication -- un
faux vert, sur le controle meme qui autorise a publier.

Un chemin vide, `.` ou `./` est refuse pour une raison differente : il est relatif et sans remontee,
mais il place tout le depot dans le perimetre, ce qui vide le controle de son sens.

L'ERREUR EST UN MANIFESTE INVALIDE, PAS UN MANQUEMENT. Elle rend les controles ininterpretables
plutot qu'elle ne revele un defaut du code livre : d'ou le code de sortie 2, et non 1.

Codes de sortie du mode ligne de commande :
    0 : tous les chemins declares sont exploitables
    2 : manifeste absent, illisible, incomplet, ou portant un chemin inexploitable
"""

from __future__ import annotations

import json
import sys
from json import JSONDecodeError
from pathlib import Path


class ManifesteInvalide(Exception):
    """Le manifeste porte un chemin que les controles ne pourront pas interpreter."""


def controler_les_chemins_declares(racine: Path, chemins_declares: list[str]) -> None:
    """
    Verifie que tout chemin declare est relatif au depot, sans remontee, et reste sous la racine.

    Leve ManifesteInvalide au premier chemin fautif, en le nommant. Ne retourne rien : il n'y a pas
    de degre dans ce controle, un manifeste inexploitable arrete tout.
    """
    for declare in chemins_declares:
        if not isinstance(declare, str) or not declare.strip():
            raise ManifesteInvalide(f"chemin vide interdit : « {declare} »")
        chemin = Path(declare)
        if chemin.as_posix() in (".", "./"):
            raise ManifesteInvalide(
                f"chemin designant la racine interdit : « {declare} » -- il place tout le depot"
                " dans le perimetre")
        if chemin.is_absolute():
            raise ManifesteInvalide(f"chemin absolu interdit : {declare}")
        if ".." in chemin.parts:
            raise ManifesteInvalide(f"remontee interdite dans un chemin : {declare}")
        try:
            (racine / chemin).resolve().relative_to(racine.resolve())
        except ValueError as erreur:
            raise ManifesteInvalide(f"chemin resolu hors du depot : {declare}") from erreur


def lire_manifeste(chemin_manifeste: Path) -> dict:
    """Lit le manifeste et verifie qu'il porte les cles que ce mode exige."""
    try:
        with chemin_manifeste.open(encoding="utf-8-sig") as fichier:
            manifeste = json.load(fichier)
    except JSONDecodeError as erreur:
        raise ManifesteInvalide(
            f"JSON invalide ligne {erreur.lineno} colonne {erreur.colno}") from erreur
    except OSError as erreur:
        raise ManifesteInvalide(f"illisible ({erreur})") from erreur

    cles_absentes = [cle for cle in ("racine_depot", "perimetre") if cle not in manifeste]
    if cles_absentes:
        raise ManifesteInvalide(
            f"cles absentes : {', '.join(cles_absentes)}. En ligne de commande, ce controle exige un"
            " perimetre a plat ; un projet dont les chemins sont repartis sur plusieurs cles appelle"
            " controler_les_chemins_declares depuis son propre controle statique")
    return manifeste


def main() -> int:
    """Point d'entree du mode ligne de commande."""
    if len(sys.argv) != 2:
        print("Usage : python verifier_chemins_declares.py <chemin_du_manifeste>", file=sys.stderr)
        return 2

    try:
        manifeste = lire_manifeste(Path(sys.argv[1]))
        chemins = [*manifeste["perimetre"]]
        if "contrat_de_correction" in manifeste:
            chemins.append(manifeste["contrat_de_correction"])
        controler_les_chemins_declares(Path(manifeste["racine_depot"]), chemins)
    except ManifesteInvalide as erreur:
        print(f"Erreur -- manifeste inexploitable : {erreur}", file=sys.stderr)
        return 2

    print("OK -- tous les chemins declares sont exploitables.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
