# Gabarit - Cadrage d'une étape

## Comment utiliser ce gabarit

Recopier la structure ci-dessous en remplaçant les blocs entre chevrons. Ne pas supprimer une
section : si elle est sans objet, l'écrire et dire pourquoi. Une section absente se lit comme un
oubli ; une section explicitement vide se lit comme une décision.

Le cadrage est écrit **pour l'agent qui rédigera l'analyse détaillée**. Son critère de complétude :
cet agent doit pouvoir travailler sans rouvrir une décision de conception, et sans reposer une
question à l'utilisateur.

Ce que le cadrage ne contient jamais : une valeur non observée, une estimation de charge, un
pseudo-code d'implémentation.

---

# Cadrage - Étape <N> - <thème>

## Rôle de ce document

<Une phrase sur ce que ce document fixe. Puis la position dans la chaîne : cadrage, analyse
détaillée, plan. Puis la liste des documents parents avec chemins absolus.>

## Phases conduites

<Les phases du pipeline effectivement exécutées, et pour chaque phase omise, la raison. Une conduite
partielle est autorisée ; une conduite partielle non annoncée est un manquement.>

## Objectif de l'étape

<Ce que l'étape livre, en termes de comportement vérifié, pas en termes de fichiers. Ce qui est
consommé de l'existant sans être modifié.>

## Périmètre

| Ligne source | Cas d'utilisation | Intention | Statut cible |
|---|---|---|---|

<Une ligne par cas d'utilisation. Le statut cible est l'un de : codé, couvert par refactorisation,
bloqué avec sa raison.>

## Décisions actées

<Une sous-section par décision, numérotée DU1, DU2, etc. Chaque décision énonce la règle, puis sa
justification en une ou deux phrases. Une décision qui ne peut pas être formulée comme une règle
applicable sans jugement n'est pas une décision : c'est une intention, à trancher avant d'écrire.>

<Si le protocole ou la doctrine du projet répond déjà à un arbitrage, ne pas le rejouer ici : le
citer par son numéro de règle. N'écrire une décision d'étape que lorsqu'elle ajoute ou restreint quelque
chose.>

## État de l'existant

<Une sous-section par élément existant touché ou consommé, numérotée E1, E2, etc. Chemin absolu,
signature ou contenu exact, et ce que l'étape en fait : consommé sans modification, étendu,
remplacé. Renvoyer au document de faits établis plutôt que de recopier ce qui y figure déjà.>

## Périmètre des modifications

### À créer

<Liste des artefacts neufs, avec leur emplacement prévu.>

### À réutiliser sans modification

<Liste explicite. Cette liste devient le périmètre gelé de la boucle de correction.>

### Hors périmètre

<Ce que l'étape ne fait pas, et pourquoi. Frontière négative : elle contraint mieux qu'une frontière
positive seule.>

## Contraintes de conception

<Contraintes vérifiables applicables à cette étape. Citer les règles du protocole et de la doctrine
de projet par leur numéro plutôt que de les recopier. N'ajouter que ce qui est spécifique à l'étape.>

## Faits à observer

| Identifiant | À observer | Canal de preuve | Ce que cela détermine | Règle de décision si le résultat diverge |
|---|---|---|---|---|

<Un identifiant par inconnue, numéroté CP1, CP2, etc. Le canal de preuve se choisit dans le relevé
d'amorçage de P0 ; une inconnue dont la couche suspecte n'a aucun canal déclaré est un
déclencheur E9, et non une invitation à improviser un canal.>

<Chaque ligne doit dire ce que l'observation rendra possible, et quelle règle s'applique selon le
résultat. Une inconnue dont la résolution demanderait un arbitrage n'est pas une observation : c'est
une décision à prendre avant.>

<Séparer ensuite, explicitement, les observations qui ne font que fournir une valeur de celles qui
peuvent infléchir une décision. Pour ces dernières, écrire la règle binaire correspondante.>

## Questions ouvertes pour l'utilisateur

<Les déclencheurs d'escalade rencontrés, ou « aucune ». Ne pas y ranger une question à laquelle la
doctrine répond.>

## Conduite à tenir quand une validation échoue

<**Section conditionnelle. Le critère est : la conduite agit-elle avant que le plan existe ?** -- et
non « aura-t-elle un plan ? ». Une conduite agit dès qu'elle écrit de l'instrumentation et lance une
exécution, c'est-à-dire dès P3, donc bien avant P5.>

<**À inclure** dans les deux cas suivants : la conduite n'aura pas de plan -- une mesure, une
observation, une investigation ne livrent aucun code ; ou la conduite aura un plan mais **observe en
P3**, puisque le plan n'existe pas encore à ce moment. **À omettre** seulement quand la conduite
n'agit pas avant P5, ce qui est rare.>

<Quand le plan existera, il portera la même section, règle RP10 de
`gabarit_plan_implementation.md`. Ce n'est pas une seconde source : les deux sont recopiées du même
original, et le contrôle statique vérifie la présence des marqueurs dans celle que le manifeste
déclare. Le manifeste désigne le cadrage tant que le plan n'existe pas, puis le plan.>

<Recopier ici le **bloc canonique** de `protocole.md`, délimité par ses deux
marqueurs `<!-- CONTRAT DE CORRECTION : DEBUT -->` et `<!-- CONTRAT DE CORRECTION : FIN -->`,
marqueurs exclus. **Tel quel, sans reformulation, sans ajout et sans retrait.**>

<**Adapter le bloc est interdit**, y compris ses deux tables. Ce qui est propre à ce chantier -- la
liste de ses fichiers, ses validations -- vit dans ce cadrage, autour du bloc, jamais dedans. La
doctrine qui entoure le bloc dans le protocole ne se recopie pas : elle sert à maintenir le
dispositif, pas à décider quoi faire au moment d'un échec.>

<Déclarer ensuite ce cadrage comme valeur de la clé `contrat_de_correction` du manifeste : le
contrôle statique y cherche les marqueurs.>

## Notes d'exécution

<**Section conditionnelle, indissociable de la précédente** : à inclure exactement quand la
précédente l'est. Une fiche par échec réel, au format fixé par `gabarit_plan_implementation.md`.>

<**Elle vit ici et non dans l'analyse détaillée, par chronologie** : une conduite partielle peut
échouer dès P3, alors que l'analyse n'est écrite qu'en P4. Loger les fiches dans l'analyse laisserait
l'exécutant sans endroit où écrire au moment précis où la règle lui interdit d'ouvrir un fichier
avant de l'avoir fait.>

<Créer la section même si aucun échec n'est attendu, et y écrire « aucun échec réel » à la clôture le
cas échéant. Une section absente se lit comme un oubli ; une section vide et datée, comme un
constat.>

## Livrables attendus de l'analyse détaillée

<Liste de ce que l'analyse doit contenir pour être complète.>

## Definition of done de l'étape

<Conditions vérifiables. Chacune doit pouvoir être contrôlée par un script, par une exécution, ou par
une lecture de fichier ; aucune ne doit reposer sur une appréciation.>
