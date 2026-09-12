# Analyse - correction du décompte des entrées ignorées

## Faits décisionnels et leur statut

| Fait observé | Source | Statut |
|---|---|---|
| Sur un lot de six entrées, le récapitulatif annonce `ignorees = 1` et `traitees = 4` | `C:\Users\hdupo\git\projet-fictif\notes\observations_decompte.md`, « Le décompte annoncé » | utilisé par la conception |
| Le témoin sans entrée illisible annonce la valeur juste | idem | utilisé par la conception : il désigne la seconde branche |
| Un fichier déposé dans le dossier de collecte porte la collecte de 413 à 414 cas | `C:\Users\hdupo\git\projet-fictif\notes\observations_decompte.md`, « L'emplacement » | utilisé par la conception |
| La commande de campagne du dépôt n'a pas été lancée | idem | contrainte prise en compte : la clôture rejoue la validation de référence, qui l'emprunte |
| Aucun consommateur ne dépend de la valeur nulle actuelle | `C:\Users\hdupo\git\projet-fictif\source\rapport\lecture.ext`, ligne 33 | écarté de la conception : le fait autorise le changement, il ne l'oriente pas |

## Décisions

### Où le compteur est incrémenté

- Ce qui est retenu : incrémenter `ignorees` dans la branche de sortie « entrée illisible », `C:\Users\hdupo\git\projet-fictif\source\collecte\recapitulatif.ext`, ligne 97, symétriquement à la ligne 82.
- Ce qui la fonde : le témoin de l'observation désigne cette branche, et elle seule.
- Ce qui a été écarté : recalculer le total à l'affichage, ligne 140. Corrigerait le symptôme sans la cause, et le fichier de lecture est hors surface.

### Ce qui fige la correction

- Ce qui est retenu : un cas de validation neuf dans `C:\Users\hdupo\git\projet-fictif\validation\collecte\recapitulatif_valid.ext`, nommé `recapitulatif_ignorees` selon la convention relevée, portant un lot de six entrées dont une rejetée et une illisible.
- Ce qui la fonde : l'emplacement est observé collectable ; la convention de nommage est relevée sur les six fichiers voisins.
- Ce qui a été écarté : réutiliser la sonde du pas 4 comme cas de validation. Elle porte deux lots dont un témoin, ce qui en fait un instrument de diagnostic et non un oracle de non-régression.

## Divergences avec le cadrage

Aucune.

## Fichiers touchés

| Chemin absolu | Créé ou modifié | Ce qui y change |
|---|---|---|
| `C:\Users\hdupo\git\projet-fictif\source\collecte\recapitulatif.ext` | modifié | incrémentation de `ignorees` ajoutée ligne 97 |
| `C:\Users\hdupo\git\projet-fictif\validation\collecte\recapitulatif_valid.ext` | créé | le cas `recapitulatif_ignorees` et son jeu de six entrées |
