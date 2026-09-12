# Conduite - correction du décompte des entrées ignorées

Document d'illustration, sur un projet fictif. Avec ses trois compagnons, il sert de **contrôle
positif** au vérificateur, par `python tests\lancer_les_tests.py` et non par un appel direct : le
vérificateur exige que la première entrée de la surface résolve vers le document contrôlé, et ces
documents portent des chemins fictifs. La suite les recopie dans un dossier temporaire et réécrit ces
seules lignes.

**Pourquoi ne pas y mettre leurs vrais chemins.** Ils lieraient le contrôle positif à l'emplacement
exact du paquet, et le casseraient au premier rangement -- alors que rien d'autre n'en dépend.

## 1. Surface d'écriture

- `C:\Users\hdupo\git\projet-fictif\notes\conduite_decompte.md`
- `C:\Users\hdupo\git\projet-fictif\notes\observations_decompte.md`
- `C:\Users\hdupo\git\projet-fictif\notes\analyse_decompte.md`
- `C:\Users\hdupo\git\projet-fictif\notes\plan_decompte.md`
- `C:\Users\hdupo\git\projet-fictif\source\collecte\recapitulatif.ext`
- `C:\Users\hdupo\git\projet-fictif\validation\collecte\recapitulatif_valid.ext`

Tout fichier absent de cette liste est en lecture seule.

## 2. Départ

- Régime d'autorisation : `C:\Users\hdupo\git\projet-fictif\doc\regime_dautorisation_standard.md`, lu le 2026-08-21
- Source de la tâche : besoin en clair donné dans le message d'ouverture
- Branche : `fix/decompte-entrees-ignorees`
- Commit de départ : `4c19ab7`
- Référentiel du projet où verser ce qui sera appris : `C:\Users\hdupo\git\projet-fictif\doc\pratiques.md`
- Comment on lance la validation : `projet valider --portee collecte`
- Où se lit le verdict : `C:\Users\hdupo\git\projet-fictif\sortie\validation\dernier.txt`
- Fichiers qu'une exécution modifie sans qu'ils appartiennent à un périmètre : `C:\Users\hdupo\git\projet-fictif\sortie\validation\`, réécrit à chaque lancement
- Validation de référence : `projet valider --portee collecte` -> vert, artefact : `C:\Users\hdupo\git\projet-fictif\sortie\validation\2026-08-21T09-14.txt`
- Si elle est rouge : sans objet, elle est verte. Le défaut n'est couvert par aucune validation existante, ce qui est précisément la raison pour laquelle il a survécu.
- Ce que la tâche fait : le récapitulatif de fin de collecte annonce zéro entrée ignorée alors que des entrées le sont. La tâche corrige le compteur et fige le comportement par une validation.
- Ce qu'elle ne fait pas : elle ne touche ni au **critère** qui décide qu'une entrée est ignorée, ni au format du récapitulatif. Les deux ont été jugés corrects et restent hors surface.

## 3. Cartographie

| Fait | Nature | Source |
|---|---|---|
| Le compteur `ignorees` est incrémenté dans la seule branche de rejet explicite | est | `C:\Users\hdupo\git\projet-fictif\source\collecte\recapitulatif.ext`, ligne 82 |
| Une entrée illisible sort par une seconde branche, qui n'incrémente rien | est | `C:\Users\hdupo\git\projet-fictif\source\collecte\recapitulatif.ext`, ligne 97 |
| Aucun consommateur du récapitulatif ne dépend de la valeur nulle actuelle | est | `C:\Users\hdupo\git\projet-fictif\source\rapport\lecture.ext`, ligne 33 |
| Les cas de validation voisins se nomment `sujet_comportement`, sans préfixe numérique | est | `C:\Users\hdupo\git\projet-fictif\validation\collecte\`, les six fichiers du dossier |
| Le nouveau code doit respecter le style existant du projet | exigé | `../../../../regles/codage.md`, section « Conventions de codage » |
| Le récapitulatif doit annoncer toute entrée non traitée, quelle qu'en soit la cause | exigé | `C:\Users\hdupo\git\projet-fictif\doc\collecte\attendus.md`, ligne 45 |

## 4. Cadrage

- Décidé : le compteur est incrémenté dans les deux branches de sortie, et non recalculé à l'affichage -- le récapitulatif lit le compteur sans le reconstruire, ligne 140, et changer cela déborderait le périmètre.
- Décidé : la correction est figée par un cas de validation neuf, nommé selon la convention relevée.
- Écarté : recalculer le total à l'affichage. Cela corrigerait le symptôme sans corriger la cause, et toucherait un fichier hors surface.
- Écarté : élargir au critère qui décide qu'une entrée est ignorée. Hors de l'objet de la tâche.
- À observer : le nombre d'entrées ignorées réellement annoncé sur un lot portant les deux causes. L'instrumentation du pas 4 le lèvera.
- À observer : l'emplacement où le cas de validation neuf doit vivre pour être collecté par la commande de campagne, sans modifier la configuration du projet.

## 5. Conduite après un échec

<!-- CONDUITE APRES ECHEC : DEBUT -->
1. Ne rien modifier tant que l'échec n'est pas écrit dans les notes d'exécution :
   ce qui a échoué, le message exact, et la cause supposée.
2. Classer l'échec, et écrire la classe retenue :
   - le code livré est fautif -> corriger le code ;
   - l'oracle porte une erreur mécanique, visible sans juger du comportement
     attendu -> corriger l'oracle ;
   - l'attendu de l'oracle est contredit par une preuve écrite AVANT l'échec
     -> corriger l'attendu, en citant cette preuve par son chemin absolu ;
   - la validité de l'oracle est douteuse sans qu'une telle preuve existe
     -> s'arrêter et rendre la main. Ne pas trancher soi-même ;
   - l'environnement ou la donnée d'entrée est fautif -> ne rien corriger,
     s'arrêter et le signaler.
3. Un attendu ne se corrige que contre une preuve antérieure à l'échec, jamais
   contre l'échec lui-même. Rendre un oracle plus permissif, le désactiver ou le
   restreindre parce qu'il vient d'échouer détruit la seule garantie de la
   conduite, et le défaut devient invisible.
4. Deux tentatives au plus sur le même échec. À la troisième, s'arrêter et rendre
   la main, en laissant l'état tel quel.
5. Ne jamais élargir la surface d'écriture pour corriger. Un correctif qui tombe
   hors surface est un arrêt, pas une extension.
<!-- CONDUITE APRES ECHEC : FIN -->

## 6. Notes d'exécution

### La validation neuve échoue sur le total, pas sur le compteur

- Étape du plan : 2
- Message exact : `attendu traitees + ignorees = 6, obtenu 5`
- Classe : erreur mécanique de l'oracle
- Ce qui a été fait : le jeu de données du cas ne portait que cinq entrées, ayant été écrit avant que le cas illisible soit ajouté. Le lot passe à six entrées. L'attendu `ignorees = 2` n'a pas bougé -- le corriger aurait relevé de la troisième classe, et aucune preuve antérieure ne l'appuyait. Le code livré n'a pas été touché.
- Statut : clos

## 7. Clôture

- Validation de référence rejouée : `projet valider --portee collecte` -> vert, artefact : `C:\Users\hdupo\git\projet-fictif\sortie\validation\2026-08-21T10-06.txt`
- Artefacts temporaires supprimés : `C:\Users\hdupo\git\projet-fictif\validation\collecte\sonde_decompte.ext`, retirée par l'étape 3 du plan
- Versé dans le référentiel du projet : une preuve rouge portant son propre témoin établit **la cause** et pas seulement le symptôme. Écrit dans `C:\Users\hdupo\git\projet-fictif\doc\pratiques.md`, section « Observations ».
- Statut de ce versement : observation datée du 2026-08-21. Aucun second contexte, donc pas de promotion en règle.
