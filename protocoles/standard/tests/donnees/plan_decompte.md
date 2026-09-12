# Plan - correction du décompte des entrées ignorées

Contrat de correction et notes d'exécution : `C:\Users\hdupo\git\projet-fictif\notes\conduite_decompte.md`

## Étape 1 - le cas de validation, rouge

- Fichiers : `C:\Users\hdupo\git\projet-fictif\validation\collecte\recapitulatif_valid.ext`, créé
- Ce qu'il faut écrire : le cas `recapitulatif_ignorees`, portant un lot de six entrées -- quatre traitables, une rejetée explicitement, une illisible. Il compare `ignorees` à `2` et `traitees + ignorees` à `6`. Aucune tolérance, aucune vérification de présence seule.
- Validation : `projet valider --portee collecte --cas recapitulatif_ignorees`
- Verdict attendu : rouge, `ignorees` valant `1` au lieu de `2`
- Où se lit le verdict : `C:\Users\hdupo\git\projet-fictif\sortie\validation\dernier.txt`

## Étape 2 - l'incrémentation manquante

- Fichiers : `C:\Users\hdupo\git\projet-fictif\source\collecte\recapitulatif.ext`, modifié
- Ce qu'il faut écrire : ligne 97, dans la branche de sortie « entrée illisible », incrémenter `ignorees` de un, exactement comme la ligne 82 le fait pour la branche de rejet explicite. Aucun autre changement dans ce fichier.
- Validation : `projet valider --portee collecte --cas recapitulatif_ignorees`
- Verdict attendu : vert, `ignorees` valant `2` et `traitees + ignorees` valant `6`
- Où se lit le verdict : `C:\Users\hdupo\git\projet-fictif\sortie\validation\dernier.txt`

## Étape 3 - retrait de la sonde

- Fichiers : `C:\Users\hdupo\git\projet-fictif\validation\collecte\sonde_decompte.ext`, supprimé
- Ce qu'il faut écrire : rien. Le fichier est supprimé, après avoir été commité à l'étape où il a été écrit.
- Validation : `projet valider --portee collecte`
- Verdict attendu : vert, et la collecte revient à 414 cas -- les 413 d'origine plus `recapitulatif_ignorees`
- Où se lit le verdict : `C:\Users\hdupo\git\projet-fictif\sortie\validation\dernier.txt`

## Retrait des artefacts temporaires

L'étape 3 supprime `C:\Users\hdupo\git\projet-fictif\validation\collecte\sonde_decompte.ext`, seule instrumentation déclarée par les observations.
