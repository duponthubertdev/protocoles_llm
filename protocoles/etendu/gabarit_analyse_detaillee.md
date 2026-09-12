# Gabarit - Analyse détaillée d'une étape

Ce fichier fait foi seul. Il porte à la fois ce que l'analyse doit accomplir et la forme qu'elle
prend. Aucun autre document ne définit ce format : deux spécifications concurrentes du même artefact
conduiraient un agent froid à suivre celle qu'il a ouverte en premier.

## Ce que l'analyse doit accomplir

Règles normatives. Une analyse qui n'en satisfait pas une n'est pas terminée.

- **RA1 - Destinataire.** L'analyse sert de base à la rédaction d'un plan par un agent faible et
  froid. Elle est écrite pour lui, pas pour son auteur.
- **RA2 - Ambiguïtés.** Lever toute ambiguïté, contradiction, incohérence ou zone d'ombre. Celle qui
  ne peut pas être levée est **déclarée bloquante**, avec son code de déclencheur d'escalade et sa
  condition de déblocage. Elle n'est jamais laissée implicite ni noyée dans une formulation
  prudente : un rédacteur froid lirait la prudence comme une décision déjà prise.
- **RA3 - Aucune décision résiduelle.** L'analyse est assez détaillée pour que le rédacteur du plan
  n'ait aucune décision à prendre. Toute alternative encore ouverte est un défaut de l'analyse.
- **RA4 - Contenu obligatoire.** Décisions actées, impacts, pièges, risques de régression et mesures
  prises pour les prévenir.
- **RA5 - Conception.** La conception respecte les **trois référentiels de conception que le
  protocole impose** -- section « Connaissances préalables, obligatoires avant P0 » -- et les
  **documents normatifs du projet énumérés par le relevé d'amorçage de P0**. Aucun chemin n'est
  répété ici : le protocole est l'autorité sur la liste universelle, le relevé sur celle du projet,
  et deux déclarations d'une même liste divergeraient à la première évolution.
- **RA6 - Exploration.** Quand il y a beaucoup de code à explorer ou à cartographier, déléguer et
  paralléliser plutôt que d'explorer soi-même. Le résultat d'une délégation est une source, pas une
  preuve : ce qui sera recopié dans l'analyse est vérifié avant usage.
- **RA7 - Écriture.** La prose de l'analyse suit la contrainte de prose relevée en P0. La
  contrainte sur les identifiants ne s'applique qu'aux symboles du programme et aux messages
  techniques.
- **RA8 - Traçabilité.** Chaque fait cite sa source : chemin absolu, et ligne quand elle existe. Une
  valeur figée cite l'observation qui l'a produite, une signature cite le fichier lu, une valeur
  attendue cite son origine.
- **RA9 - Rien d'inventé.** Aucune valeur non observée n'est écrite, même assortie d'un
  conditionnel. En l'absence d'observation, écrire que l'observation manque et s'arrêter là.
- **RA10 - Validation définie d'avance.** L'analyse écrit ce qui vaudra validation, avant toute
  exécution. Un résultat jugé après coup est jugé favorablement.

Les règles RA8 à RA10 existent parce que ce protocole ne comporte pas de relecture humaine entre
l'analyse et le plan. Dans une chaîne où un humain relit, l'invention et l'ambiguïté se voient à la
lecture ; ici, rien ne les voit. Elles remplacent ce filet par des propriétés vérifiables.

## Comment utiliser ce gabarit

Recopier la structure ci-dessous en remplaçant les blocs entre chevrons. Ne pas supprimer une
section : si elle est sans objet, l'écrire et dire pourquoi. Une section absente se lit comme un
oubli, une section explicitement vide se lit comme une décision.

---

# Analyse détaillée - Étape <N> - <thème>

## Objet et audience

<Ce que cette analyse tranche, et ce qu'elle suppose déjà lu. Chemin absolu du cadrage dont elle
découle.>

## Périmètre

<Reprise du périmètre du cadrage, sans le réinterpréter. Toute divergence est signalée comme une
correction explicite, avec sa raison.>

## Faits observés

| Identifiant | Ce qui a été observé | Source | Statut | Conséquence |
|---|---|---|---|---|

<Un identifiant par observation du cadrage. La source est un chemin absolu, avec la ligne quand elle
existe. Une observation non réalisée s'écrit « non observée », avec sa conséquence sur le périmètre
et son code d'escalade -- jamais avec une valeur supposée.>

<Le **statut** vaut l'un de trois mots exactement : « utilisé par la conception », « contrainte prise
en compte », ou « écarté », suivi de sa raison. La table ne contient pas que les observations du
cadrage : **tout fait décisionnel y entre**, c'est-à-dire tout fait d'observation qui pourrait
infléchir une valeur, un oracle ou une structure de scénario, même s'il n'avait pas été anticipé
comme une inconnue. L'analyse n'est pas close tant qu'un fait décisionnel reste sans statut.>

<L'exigence est bornée aux faits décisionnels. Recopier chaque ligne d'observation brute produirait
du remplissage mécanique, sans valeur. Le critère de tri est « ce fait pourrait-il changer une
décision déjà prise ? » : s'il le pourrait, il entre.>

## Décisions de conception

<Une sous-section par décision, numérotée D1, D2, etc. Chaque décision énonce le choix retenu, les
options écartées et la raison de l'écart. Une décision sans option écartée est souvent une décision
non prise.>

## Conception cible, fichier par fichier

<Une sous-section par fichier, avec son chemin absolu et son statut : créé, modifié, supprimé.>

<Pour un fichier créé : son contenu, ou la partie déterminante de son contenu.>

<Pour un fichier modifié : ce qui change exactement, et ce qui ne change pas.>

<Le relevé d'amorçage de P0 nomme les artefacts du projet ; l'analyse dit ce que chacun doit
porter. S'y conformer plutôt que d'inventer un niveau de détail.>

## Correspondance oracle

| Élément vérifié | Moyen de vérification | Origine de l'attendu | Valeur attendue | Source de la valeur |
|---|---|---|---|---|

<Une ligne par assertion. Une assertion dont la valeur attendue n'a pas d'origine traçable est une
assertion à supprimer, ou une donnée à produire.>

## Impacts

<Ce que l'étape change pour le reste du dépôt : appelants existants, contrats partagés, artefacts
consommés ailleurs. Si l'étape n'impacte rien hors de son périmètre, l'écrire.>

## Pièges

<Ce qui a déjà mal tourné, ou ce qui a une forte probabilité de mal tourner, formulé comme un
interdit concret plutôt que comme une mise en garde. Un piège sans conduite à tenir n'est pas
exploitable.>

## Risques de régression et mesures

| Risque | Ce qui pourrait casser | Mesure de prévention | Comment on le saura |
|---|---|---|---|

<Si l'étape ne modifie rien d'existant, l'écrire et le justifier par la liste des fichiers touchés.>

## Validations prévues

<Ce qui sera exécuté, dans quel ordre, et le résultat exact qui rendra chaque validation concluante.
Ce résultat est défini ici, avant l'exécution.>

## Ce que cette analyse ne fait pas

<Frontière négative explicite, reprise et précisée depuis le cadrage.>

## Chemins absolus des fichiers touchés

<Liste plate, exhaustive. Elle devient la surface d'écriture autorisée de la phase d'implémentation,
et le périmètre déclaré par le manifeste du contrôle statique.>
