# Protocole standard - production d'une évolution par un agent LLM

## Ce que c'est

La méthode à suivre pour produire une évolution, **quelle que soit son ampleur**. Il n'abandonne rien
de ce qu'une conduite sérieuse exige -- cartographie, cadrage, observation, analyse, plan, mémoire,
gouvernance. Il est allégé sur la **forme**, jamais sur le fond.

Ce qui est allégé : **quatre documents** au lieu de huit artefacts et d'un manifeste, leurs squelettes
portés par ce document au lieu de cinq gabarits séparés, **un** contrôle mécanique au lieu de trois.

Il est **technologiquement neutre** : il ne nomme aucun langage, aucun outil, aucune commande. Ce qui
dépend du dépôt se relève au départ et s'écrit dans le document de conduite. Les référentiels qu'il
impose portent, eux, quelques exemples liés à une technologie -- ce sont des exemples, pas des
conditions d'application.

Un seul document de méthode : celui-ci. **Trois référentiels normatifs se lisent en plus**, avant
toute conduite -- ils sont nommés plus bas.

**Ce que ce protocole ne fait pas.** Il ne dispense d'aucune revue et ne remplace aucun jugement
humain. Il rend un travail auditable à coût faible ; il ne certifie rien.

## Ce que le projet doit fournir

**Une seule chose écrite d'avance : le régime d'autorisation.** Tout le reste, l'agent le trouve en
regardant et le consigne au pas 1.

La raison de cette asymétrie : une permission **ne se découvre pas, elle se donne**. Pré-répondre aux
autres questions -- comment on lance, où se lit le verdict -- produirait une synthèse de plus, qui
vieillirait sans que rien ne le signale.

**Le protocole standard possède son propre régime**, dans `doc/regime_dautorisation_standard.md`. Ce
fichier court et distinct vit à côté de la documentation du projet, jamais dedans.

La dépendance va dans un seul sens : ce fichier cite la documentation du projet, l'inverse jamais.
Une synthèse d'architecture est lue par des agents qui font tout autre chose, et doit rester juste si
ce protocole n'est pas employé.

```markdown
## Régime d'autorisation de l'agent -- protocole standard

Décisions du propriétaire du dépôt, <date>. Chacune se retire en modifiant sa ligne.

| Décision | Valeur |
|---|---|
| Pré-autorisation des outils du CLI | <complète, par la commande exacte ; ou liste fermée ; ou aucune> |
| Création du ticket par l'agent | <autorisée, et où vit le mode d'emploi ; ou non autorisée> |
| Publication de la branche du sujet | <autorisée, et à quelles conditions ; ou non autorisée> |
| Branches principales du dépôt | <leurs noms exacts> |
| Convention de nommage des branches | <la convention, ou : celle du protocole> |
| Exceptions aux référentiels | <aucune ; ou la règle écartée, avec sa raison et sa date> |
```

**Absent, ou muet sur un point nécessaire, c'est un arrêt.** L'agent ne le complète pas lui-même : il
appartient au propriétaire du dépôt. Chaque décision porte sa date, et se retire en modifiant sa
ligne.

**Convention de branche par défaut**, quand le régime ne dit rien : `<type>/<sujet>`, le type pris
dans `feat`, `fix`, `docs`, `chore`.

## Les cinq règles

Elles tiennent à chaque instant, et rien de ce qui suit ne les suspend.

- **R1 -- Le verdict ne vient jamais de l'agent.** Ce qui dit qu'une tâche est faite est un oracle
  externe exécutable, dont le verdict se lit dans un artefact. Une relecture de son propre travail
  n'est pas une validation : elle confirme ce qui ressemble à du travail fini.

- **R2 -- Aucune valeur n'est écrite si elle n'a pas été établie.** Une valeur s'établit de trois
  façons, et la façon dépend de la **nature** du fait :

  | Nature du fait | Ce qui l'établit, et rien d'autre |
  |---|---|
  | Ce que le code **est** : chemin, signature, structure, valeur littérale | Le code lui-même, ouvert et cité par son chemin absolu -- jamais une synthèse qui le décrit |
  | Ce que le système **fait** : valeur produite, verdict, comportement | Une exécution observée, citée par l'artefact qui porte sa sortie |
  | Ce qui est **exigé** : attendu, règle métier, contrainte | La source qui fait autorité pour l'exiger, nommée par son chemin absolu |

  Lire ne suffit donc pas : une valeur de comportement trouvée dans une documentation n'est pas
  observée, et une exigence tirée du code n'est pas exigée. Un fait qu'aucune des trois voies
  n'établit s'écrit `ABSENT`, jamais sous forme d'une valeur plausible assortie d'un conditionnel.

  Avant d’écrire, les valeurs, les décisions et les limites que l’écriture engage se relisent à leur
  source. Ni un souvenir ni un résumé de conversation n’en tient lieu. Ce qui manque se traite par
  les règles existantes d’inconnue et d’arrêt.

- **R3 -- L'écriture est bornée à chaque pas, et déclarée avant d'écrire.** Chaque pas n'écrit que
  les documents que la table des surfaces lui attribue ; tout le reste est en lecture seule. Dans sa
  surface, l'agent agit sans demander d'autorisation.

  **C'est cette règle, et non une prescription d'ordre, qui empêche une phase d'en rouvrir une
  autre.** L'analyse ne peut pas contredire le cadrage parce qu'elle n'a pas le droit d'écrire
  dedans.

  **Le document de conduite est la première entrée de sa propre surface**, inscrite dans le squelette
  même qui l'ouvre : il est le premier fichier que la conduite touche.

- **R4 -- Un échec d'oracle s'écrit avant d'être corrigé.** Après le rouge d'une validation portant
  sur **le travail livré**, rien n'est modifié tant que l'échec n'est pas consigné et classé. C'est
  l'étape que la complétion saute naturellement : sans elle, le premier réflexe est de modifier le
  code testé jusqu'à obtenir du vert.

  **Le contrôle de conformité des documents ne relève pas de cette règle.** Il porte sur les
  documents et non sur le travail livré, il se joue au pas 8, et il n'ouvre aucune note d'exécution.

- **R5 -- Ce qui dépasse le cadre s'arrête.** Il n'y a pas d'extension silencieuse du périmètre, ni
  de règle inventée en cours de route. Un dépassement rend la main au propriétaire, avec l'état
  laissé tel quel.

## Correctifs

Pour un correctif, établir une preuve du défaut avant modification : reproduction contrôlée si
elle est sûre et possible, sinon artefact existant explicitement rattaché au défaut. Après correction,
vérifier le comportement attendu et la non-régression pertinente. Si la preuve est insuffisante,
rendre la main selon les règles d'arrêt du protocole.

L'amorçage sans validation initiale ne dispense pas de prouver le défaut à corriger.

## Exigence de conception greenfield

Les évolutions et les corrections sont menées en mode greenfield : satisfaire entièrement le besoin
établi et traiter les causes identifiées au bon niveau d'abstraction, sans reproduire une mauvaise
conception au motif qu'elle existe déjà. La réduction du nombre de modifications ne justifie ni
pansement local, ni oracle insuffisant ou affaibli, ni attente arbitraire, ni sélecteur fragile choisi
par facilité. Les refactorisations nécessaires sont incluses dans les limites du périmètre déclaré
et de la surface d'écriture autorisés ; les améliorations indépendantes du besoin restent hors
périmètre et se consignent selon les règles de transmission du protocole. **Cette exigence n'élargit
ni le périmètre ni la surface d'écriture autorisés et ne modifie aucune règle de traitement des
anomalies ou d'arrêt du protocole.**

## Les référentiels de conception et de codage

**Trois documents sont normatifs pour tout ce que la conduite écrit.** Ils ne sont pas désignés par
le projet et ne se redéclarent nulle part : ce protocole les impose, et un projet n'a rien à fournir
pour qu'ils s'appliquent.

| Document | Ce qu'il régit |
|---|---|
| `../../referentiels/conception.md` | La conception : principe central, KISS, DRY, YAGNI, responsabilité unique, cohésion et couplage, OCP, séparation modèle métier et orchestration, évitement du null, immuabilité, fonctions pures, état borné, testabilité, composition, gestion des erreurs, fail fast |
| `../../referentiels/conception_de_code_pour_llm.md` | La conception LLM-friendly, **parce que le LLM est l'outil d'assistance principal du développeur** : réduction de la variance, dépendances explicites, patterns consistants, unités analysables dans une fenêtre réduite, absence de magie implicite |
| `../../referentiels/codage.md` | Le code écrit : commentaires, conventions de codage, jeu de caractères, conventions git, nommage des modules, types, fonctions et variables, documentation obligatoire |

**Ils se lisent en précondition, avant le pas 1.** Ils régissent aussi les documents de la conduite --
commentaires, jeu de caractères, documentation, messages de commit --, et le document de conduite est
le premier fichier écrit : les lire plus tard reviendrait à ne les appliquer qu'à partir du deuxième.

C'est aussi le point qui coûte le plus cher quand on l'oublie : leurs règles infléchissent ce qu'on
décide de faire, pas seulement la forme de ce qu'on a fait. YAGNI ne se rattrape pas après coup, et
une convention de nommage découverte à la relecture se paie en réécriture.

**Ils ne se recopient pas dans les documents, et ne se résument pas.** Un résumé serait une seconde
source qui vieillirait sans que rien ne le signale, et un agent qui lit le résumé croirait
légitimement avoir tout lu.

`../../referentiels/conception.md` renvoie lui-même à `../../referentiels/gestion_des_erreurs.md` pour la hiérarchie d'exceptions et le
logging : ce renvoi fait partie du référentiel et se suit quand la tâche touche au traitement des
erreurs.

**Ce que le dépôt impose en plus reste dû** -- contrôle statique, style, typage. Ces trois documents
ne les remplacent pas.

Les références relatives de cette section se résolvent depuis le dossier de ce fichier de
protocole, jamais depuis le répertoire courant. Avant de les lire, les convertir en chemins absolus
et vérifier leur existence ; une référence introuvable est un arrêt.

## Les quatre documents

| Document | Ce qu'il porte | Grossit avec la tâche |
|---|---|---|
| `conduite_<theme>.md` | Départ, cartographie, cadrage, conduite après échec, notes d'exécution, clôture | non |
| `observations_<theme>.md` | Les faits observés, chacun avec son artefact d'exécution | oui |
| `analyse_<theme>.md` | Les valeurs figées, la descente au niveau fichier | oui |
| `plan_<theme>.md` | Les étapes, exécutables sans décision restante | oui, le plus |

Ils vivent côte à côte, dans le dossier que le dépôt réserve à ses notes de projet.

**Pourquoi le contrat de correction et les notes d'exécution vivent dans la conduite et non dans le
plan.** Une conduite agit dès le pas 4 -- une instrumentation, une exécution --, bien avant qu'un plan
existe. Les loger dans le plan laisserait l'exécutant sans conduite à tenir pendant la moitié du
travail. Et le plan reste ainsi un plan : un agent qui l'exécute n'y lit pas les échecs des autres.

**Pourquoi le document de conduite ne grossit pas.** Il ne contient aucune énumération dont la
longueur dépend de la tâche. C'est lui qu'on rouvre le plus souvent ; il doit rester manipulable.

## La marche à suivre

Huit pas, dans cet ordre. Un pas ne commence pas tant que l'artefact du précédent n'existe pas.

**La table des surfaces est la règle, le texte l'explique.**

| Pas | Ce qu'il écrit, et rien d'autre |
|---|---|
| 1. Ouvrir | `conduite` : squelette, surface, départ |
| 2. Cartographier | `conduite` : section cartographie |
| 3. Cadrer | `conduite` : section cadrage |
| 4. Observer | `observations`, et l'instrumentation probatoire déclarée |
| 5. Analyser | `analyse` |
| 6. Planifier | `plan` |
| 7. Exécuter | les fichiers énumérés par le plan, **plus** `conduite` : notes d'exécution |
| 8. Clore | `conduite` : section clôture, **plus** le référentiel du projet |

**1. Ouvrir.** Lire le régime d'autorisation ; absent ou muet, s'arrêter. Si la tâche est donnée par
un ticket, le lire avant de cadrer le travail et consigner son URL ainsi que sa date de consultation ;
s'il est inaccessible, s'arrêter. Vérifier que la branche courante est une branche du sujet et non
une branche principale.

Le **premier contenu écrit** dans `conduite_<theme>.md` est un squelette : tous ses titres de
section, portant déjà son propre chemin absolu en première entrée de « Surface d'écriture » et la
conduite après échec recopiée telle quelle, **et aucun autre champ renseigné**. C'est une seule
écriture, et rien d'autre ne s'écrit avant elle.

Puis remplir « Départ » : branche, commit courant, commande et verdict de la validation de référence
avec le chemin absolu de son artefact, et ce que la tâche fait -- **et ne fait pas**.

**Une validation de référence rouge n'est pas toujours un arrêt.** Rouge *parce qu'elle expose le
défaut traité*, c'est la preuve rouge du pas 4 : elle s'écrit aux deux endroits, et la conduite
continue. Rouge pour une cause étrangère à la tâche, c'est un arrêt, parce que plus aucun écart
constaté ensuite ne serait imputable au travail.

**Amorçage sans validation initiale.** Si le projet ne possède encore aucune validation exécutable,
consigner `ABSENT` au départ et prévoir la création du premier contrôle dans la surface autorisée.
Son attendu est fixé avant l'implémentation du comportement contrôlé. À la clôture, exécuter la
validation ainsi créée : l'absence de validation initiale ne dispense pas de validation finale.
Si aucun contrôle pertinent ne peut être défini, rendre la main.

**2. Cartographier.** Rassembler les faits nécessaires au cadrage, sans les redécouvrir plus tard.
L'exploration large peut être déléguée à des sous-agents en parallèle, avec une consigne fermée :
recopier, sourcer par chemin absolu, écrire `ABSENT`, ne rien recommander.

**Un rapport de sous-agent est une source, pas une preuve.** Deux modèles de la même famille
partagent les mêmes angles morts. Ce qui sera recopié -- signatures, chemins, valeurs exactes -- se
vérifie avant usage.

Un plan ou une spécification rédigés hors de ce protocole se consomment **ici**, comme n'importe quel
document existant, et n'ont aucune autorité.

**La convention se relève en deux faits, jamais en un.** Ce que montrent les fichiers voisins est de
nature *est*, et se source sur ces fichiers. L'obligation de s'y conformer est de nature *exigé*, et
se source sur `../../referentiels/codage.md`. Quand les deux divergent, l'écart se signale plutôt qu'il ne se
propage.

**3. Cadrer.** Fixer ce qui est décidé, énumérer ce qui reste à observer. Le cadrage **ne contient
aucune valeur non observée**. Son critère de complétude : l'analyse doit pouvoir être écrite sans
rouvrir une décision de conception.

**4. Observer.** Lever chaque inconnue du cadrage par une observation réelle, produite par une
instrumentation exécutée comme une exécution normale. Pour une correction d'anomalie, consigner
ici la **preuve rouge** selon la règle « Correctifs » : reproduction contrôlée ou artefact existant.

**Observer coûte, et ce coût se choisit.** Une observation qui n'exige pas de donnée fraîche se fait
sur la variante la plus courte qui pointe une donnée déjà produite. **On itère sur le court, on valide
sur le complet** : un vert sur variante courte atteste un comportement sur une donnée préparée, pas
la séquence que le périmètre déclare.

Une observation impossible se déclare bloquée ; la ligne concernée n'est jamais complétée par une
valeur plausible.

**5. Analyser.** Résoudre les inconnues à partir des observations, figer les valeurs, descendre au
niveau fichier. Chaque valeur figée cite l'observation dont elle provient.

**Tout fait décisionnel reçoit un statut explicite** : utilisé par la conception, contrainte prise en
compte, ou écarté avec sa raison. L'analyse n'est pas close tant qu'un fait décisionnel reste sans
statut. Le sourçage n'attrape pas ce défaut-là : une décision peut être prise, complète, et fausse au
regard d'un fait déjà relevé.

**6. Planifier.** Écrire un plan exécutable par un agent froid : aucune décision de conception
restante, aucun choix à faire. Il énumère les fichiers à créer ou modifier avec leur chemin absolu,
et ce que chaque étape valide.

Le plan **ne contient aucune commande de gestion de version comme étape de travail** : les points de
commit sont une obligation permanente, pas une décision à rejouer dans chaque plan.

**7. Exécuter.** Appliquer le plan. Pour chaque étape : contrôle statique du projet, compilation ou
équivalent, puis exécution. La surface d'écriture est exactement l'ensemble des fichiers énumérés par
le plan ; tout autre fichier est en lecture seule. Un rouge ouvre la conduite après échec, et rien
d'autre.

**8. Clore.** Cinq actions, dans cet ordre, et le commit vient **en dernier** :

1. rejouer la validation de référence, et consigner son verdict avec le chemin de son artefact ;
2. supprimer les artefacts temporaires -- ils ont déjà été commités, c'est ce qui rend leur existence
   vérifiable après coup ;
3. remplir « Clôture », **et verser ce qui a été appris dans le référentiel du projet** ;
4. lancer le contrôle. Rouge, corriger le document et **le relancer**, jusqu'au vert ou jusqu'au
   deuxième échec, qui est un arrêt ;
5. le contrôle étant vert, commiter **l'état final de toute la surface**, suppressions comprises.

**Commiter avant de contrôler produirait un commit dont rien n'atteste la conformité**, puis une
correction que rien ne recommitterait. L'état vert et l'état commité seraient deux états différents,
et c'est le second qui reste.

Après ce commit, appliquer la règle « Publication de la branche du sujet ».

### Ce qui est appris ne meurt pas avec la conduite

La clôture verse dans **le référentiel du projet** -- celui relevé au pas 1 -- ce que la conduite a
appris. Une seule destination : ce protocole ne capitalise pas sur lui-même.

**Le seuil est fermé.** Ce qui est appris entre comme **observation**, datée. Cela devient une
**règle** à trois conditions cumulatives : réutilisabilité démontrée hors du cas qui l'a fait naître,
absence de règle équivalente déjà présente, confirmation sur un second contexte. À défaut, cela reste
une observation et se tranche à la consolidation suivante : promue ou retirée.

Consigner coûte peu ; promouvoir engage le lecteur suivant. Sans échéance, la distinction devient
nominale : tout reste, et un référentiel qui grossit sans critère finit illisible.

Une conduite qui ne remonte rien l'écrit aussi : c'est un constat, pas un silence.

## Quand rendre la main

Ces situations ne se contournent pas et ne se traitent pas dans ce protocole. L'agent **s'arrête**,
écrit dans la conduite ce qu'il a constaté, et rend la main sans défaire ce qui est déjà commité.

| Situation | Pourquoi c'est un arrêt |
|---|---|
| Le régime d'autorisation est absent, ou muet sur un point nécessaire | Une permission ne se devine pas. L'agent ne se donne pas ce qu'il n'a pas reçu |
| Un référentiel déclaré est introuvable ou illisible | La conduite s'appuierait sur une règle qu'elle n'a pas lue |
| La branche courante est une branche principale | Le travail vit sur une branche du sujet, sans exception |
| Un fichier hors de la surface du pas courant doit être modifié | La surface est la garantie ; l'étendre en cours de route la supprime |
| La validation de référence est rouge pour une cause **étrangère au défaut traité** | Aucun écart constaté ensuite ne serait imputable au travail |
| La source d'exigence et le comportement observé se contredisent **hors de l'objet de la tâche** | C'est un défaut de plus, que personne n'a décidé de traiter |
| Un fait nécessaire à une décision reste introuvable | R2 interdit de le combler ; poursuivre reviendrait à inventer |
| Deux tentatives de correction du même échec ont échoué | Au-delà, la correction devient de la recherche, et la surface se met à enfler |
| Une action non réversible, ou hors du périmètre déclaré, serait nécessaire | Elle appartient au propriétaire, pas à l'agent |

Rendre la main n'est pas un échec de la conduite : c'est le cas nominal quand la tâche n'était pas
celle qu'on croyait. Le seul vrai défaut est de continuer sans le dire.

## Ce que l'agent fait avec l'historique

Il **ajoute de l'état récupérable**, et rien d'autre. Il n'en détruit aucun.

- Commiter est autorisé et attendu, sur la branche du sujet : à chaque pas dont l'artefact est
  achevé, après chaque étape verte du plan, et au pas 8 -- ce dernier **une fois le contrôle vert**,
  jamais avant.
- Un artefact temporaire est commité **avant** d'être supprimé : c'est ce qui rend son existence
  vérifiable après coup.
- **Sont interdits sans instruction explicite du propriétaire** : réécrire l'historique, supprimer ou
  déplacer de force une référence, fusionner vers une branche principale, abandonner des
  modifications non commitées.

### Publication de la branche du sujet

À la clôture, l'exécutant publie la branche du sujet si le régime d'autorisation le permet, si aucun
arrêt ne reste à résoudre, si les validations exigées et le vérificateur de documents passent, et si
les changements de la conduite sont commités sur la branche déclarée. Sinon, il conserve la branche
locale et indique ce qui empêche sa publication. Publier n'autorise pas à fusionner.

## Les squelettes

Recopier la structure en remplaçant les blocs entre chevrons. **Ne supprimer aucune section** : une
section sans objet porte la mention `Sans objet` et sa raison, une section vide est indiscernable
d'un oubli.

<!-- SQUELETTES : DEBUT -->

### `conduite_<theme>.md`

```text
# Conduite - <thème>

## 1. Surface d'écriture

- <chemin absolu de ce document, toujours en première entrée>
- <un chemin absolu par ligne, chacun écrit avant que le fichier soit touché>

Tout fichier absent de cette liste est en lecture seule.

## 2. Départ

- Régime d'autorisation : <chemin absolu>, lu le <date>
- Source de la tâche : <besoin en clair, chemin absolu, ou URL HTTPS du ticket et date de consultation>
- Branche : <nom de la branche du sujet>
- Commit de départ : <identifiant du commit>
- Référentiel du projet où verser ce qui sera appris : <chemin absolu>
- Comment on lance la validation : <commande exacte>
- Où se lit le verdict : <chemin absolu de l'artefact>
- Fichiers qu'une exécution modifie sans qu'ils appartiennent à un périmètre : <chemins absolus entre backticks, ou : aucun>
- Validation de référence : <commande> -> <verdict>, artefact : <chemin absolu>
- Si elle est rouge : <cause étrangère, donc arrêt | expose le défaut traité, donc c'est la preuve rouge | sans objet, elle est verte>
- Ce que la tâche fait : <une à trois lignes>
- Ce qu'elle ne fait pas : <ce qui est volontairement laissé de côté>

## 3. Cartographie

| Fait | Nature | Source |
|---|---|---|
| <le fait, nommé par sa valeur> | <est, fait, ou exigé> | <chemin absolu, et ligne si elle existe> |

<un fait nécessaire mais non établi s'écrit ABSENT dans la colonne de gauche>

## 4. Cadrage

- Décidé : <une décision par ligne, chacune avec ce qui la fonde>
- Écarté : <ce qui a été envisagé puis écarté, avec la raison>
- À observer : <une inconnue par ligne, avec ce qui la lèvera>

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

<une entrée par échec, ou la seule mention : Aucun échec.>

### <ce qui a échoué>

- Étape du plan : <numéro, ou : hors plan>
- Message exact : <recopié, pas résumé>
- Classe : <code livré, erreur mécanique de l'oracle, attendu contredit par une preuve antérieure, validité douteuse, ou environnement>
- Ce qui a été fait : <l'action, ou : arrêt>
- Statut : <clos, ou : arrêt rendu au propriétaire>

## 7. Clôture

- Validation de référence rejouée : <commande> -> <verdict>, artefact : <chemin absolu>
- Artefacts temporaires supprimés : <liste des chemins, ou : aucun>
- Versé dans le référentiel du projet : <ce qui a été écrit, et où ; ou : rien, et pourquoi>
- Statut de ce versement : <observation datée, ou : règle, avec le second contexte qui l'a confirmée>
```

### `observations_<theme>.md`

```text
# Observations - <thème>

## Dispositif

- Instrumentation employée : <chemins absolus des fichiers écrits pour observer, ou : aucune>
- Comment elle a été exécutée : <commande exacte>
- Retrait prévu : <l'étape du plan qui la supprime, ou : elle reste livrée>

## <l'inconnue du cadrage que cette observation lève>

- Ce qui a été observé : <la valeur ou le comportement, exact>
- Artefact d'exécution : <chemin absolu>
- Témoin : <ce que le même dispositif rend sur un cas où le phénomène ne doit pas se produire, ou : sans objet, et pourquoi>
- Conclusion : <ce que l'observation établit, et ce qu'elle n'établit pas>

<une section par inconnue ; une inconnue non levée porte BLOQUÉE, et l'obstacle>
```

### `analyse_<theme>.md`

```text
# Analyse - <thème>

## Faits décisionnels et leur statut

| Fait observé | Source | Statut |
|---|---|---|
| <le fait> | <chemin absolu de l'observation> | <utilisé par la conception, contrainte prise en compte, ou écarté avec sa raison> |

## Décisions

### <la décision, nommée par ce qu'elle tranche>

- Ce qui est retenu : <la solution, au niveau fichier>
- Ce qui la fonde : <les faits ci-dessus, par leur intitulé>
- Ce qui a été écarté : <les autres options, avec leur raison>

## Divergences avec le cadrage

<toute décision qui s'écarte du cadrage, avec sa raison ; ou : aucune>

## Fichiers touchés

| Chemin absolu | Créé ou modifié | Ce qui y change |
|---|---|---|
```

### `plan_<theme>.md`

```text
# Plan - <thème>

Contrat de correction et notes d'exécution : <chemin absolu du document de conduite>

## Étape <n> - <ce qu'elle produit>

- Fichiers : <chemins absolus, créés ou modifiés>
- Ce qu'il faut écrire : <assez précis pour qu'aucun choix ne reste>
- Validation : <commande exacte>
- Verdict attendu : <valeur observable exacte, pas une impression>
- Où se lit le verdict : <chemin absolu>

<une section par étape ; l'ordre est celui de l'exécution>

## Retrait des artefacts temporaires

<l'étape qui supprime chaque instrumentation déclarée dans les observations, ou : aucun artefact temporaire>
```

<!-- SQUELETTES : FIN -->

**Le champ `Statut` des notes d'exécution est fermé.** Il vaut `clos` ou `arrêt rendu au
propriétaire`, une seule fois par entrée.

## Le contrôle

Une commande, au pas 8. Elle porte sur les documents, jamais sur le code livré.

```text
python verifier_documents.py <chemin absolu du document de conduite>
```

Ce qu'elle vérifiera : la présence et l'ordre des sections de chaque document, la première entrée de
la surface, l'identité de la conduite après échec avec le canon de ce protocole, l'absence de bloc
laissé à remplir, le statut unique et fermé de chaque note d'exécution, et l'appartenance à la surface
de tout chemin visible par Git depuis le commit de départ. Le document de conduite, sa surface et ses
sorties techniques appartiennent à ce même dépôt.

Le vérificateur a sa propre suite, qui exerce le cas conforme et les états interdits sur les
quatre documents de `tests/donnees/`. Ils illustrent une conduite fictive ; les exigences restent
définies par le protocole.

```text
python tests\lancer_les_tests.py
```

**Une cible introuvable fait échouer le contrôle en la nommant.** Un contrôle qui répondrait « aucun
manquement » parce qu'il n'a rien trouvé à examiner serait un faux vert, et c'est le plus dangereux :
il se présente comme une preuve.

## Le message qui ouvre la conduite

```text
Applique le protocole spécifié ici :
  <chemin absolu de ce fichier protocole.md>

Le projet est décrit ici :
  <chemin absolu de la documentation du projet>

Le régime d'autorisation propre au protocole standard est ici :
  <chemin absolu du projet>\doc\regime_dautorisation_standard.md

La tâche :
  <le besoin, le chemin absolu du document qui le décrit, ou l'URL HTTPS du ticket>
```

Rien d'autre n'entre dans ce message. En particulier :

- **aucune formule qui donne autorité à un document** -- « source de vérité » se lit comme une
  dispense de vérifier, et le défaut qu'elle produit est invisible puisque la vérification est
  précisément ce qui aura été sauté. Un document cité **délimite le travail** ; son contenu reste
  soumis à R2 ;
- **aucune règle de méthode** -- elle appartient à ce document ;
- **aucune permission** -- elle appartient au régime d'autorisation ;
- **rien que l'agent trouvera en regardant** -- commandes, chemins, artefacts de verdict : cela se
  relève au pas 1.

**Quand un document cité contredit le code**, la réponse dépend de la nature du fait :

| Ce sur quoi porte la contradiction | Ce qui tranche |
|---|---|
| Ce que le code **est** -- structure, signature, chemin | Le code observé. Un document descriptif périmé ne fait pas règle |
| Ce que le système **doit faire** -- attendu, règle métier | Personne, sur le moment. Si cette contradiction **est** l'objet de la tâche, c'est le défaut à corriger, et le document dit l'attendu. Sinon, c'est un arrêt |

Faire primer le code sur une exigence reviendrait à déclarer conforme tout comportement observé --
c'est-à-dire à rendre toute correction d'anomalie impossible à motiver.

**Avant de lancer**, trois vérifications d'une minute : les chemins cités existent, le ticket éventuel
est accessible, et l'arbre de travail est propre.

## Ce que ce protocole ne garantit pas

- **Il ne remplace pas la revue humaine.** Il rend le travail auditable ; il ne dit pas qu'il est bon.
- **La conformité aux trois référentiels n'est couverte par aucun contrôle.** Rien ne vérifie qu'ils
  ont été lus, ni qu'ils ont été suivis.
- **Le contrôle de surface voit ce que Git voit.** Il ne détecte ni un fichier ignoré, ni une
  modification temporaire jamais commitée puis entièrement annulée.
- **Il ne rejoue rien.** Une validation verte obtenue ici ne protège la suite que si le dépôt la
  reprend dans ce qui tourne à chaque fois. Le pas 8 ne le vérifie pas.
- **L'ordre des pas n'est pas attesté.** Rien ne prouve qu'une section a été écrite avant la
  suivante ; seul le commit par pas en laisse la trace.
