# Observations - correction du décompte des entrées ignorées

## Dispositif

- Instrumentation employée : `C:\Users\hdupo\git\projet-fictif\validation\collecte\sonde_decompte.ext`
- Comment elle a été exécutée : `projet valider --portee collecte --cas sonde_decompte`
- Retrait prévu : étape 3 du plan

## Le décompte annoncé sur un lot portant les deux causes

- Ce qui a été observé : sur un lot de six entrées dont une rejetée et une illisible, le récapitulatif annonce `ignorees = 1` et `traitees = 4`. Le total est donc de cinq, pour six entrées soumises.
- Artefact d'exécution : `C:\Users\hdupo\git\projet-fictif\sortie\validation\2026-08-21T09-31.txt`
- Témoin : sur un lot identique sans entrée illisible, le même dispositif annonce `ignorees = 1` et `traitees = 4`, total cinq pour cinq entrées -- la valeur juste. C'est donc la seconde branche de sortie qui est en cause, et non le compteur en général.
- Conclusion : établit que l'entrée illisible n'est comptée nulle part. N'établit rien sur les autres causes de rejet, qu'aucun lot n'a exercées ici.

## L'emplacement où un cas de validation neuf est collecté

- Ce qui a été observé : un fichier déposé dans `C:\Users\hdupo\git\projet-fictif\validation\collecte\` fait passer la collecte de 413 à 414 cas, sans modification de la configuration du projet.
- Artefact d'exécution : `C:\Users\hdupo\git\projet-fictif\sortie\validation\2026-08-21T09-38.txt`
- Témoin : le même fichier déposé un niveau au-dessus laisse la collecte à 413. L'emplacement est donc bien la cause du rattachement, et non la simple existence du fichier.
- Conclusion : établit l'emplacement à employer. N'établit pas que la commande de campagne du dépôt emprunte le même chemin de collecte -- elle n'a pas été lancée ici.
