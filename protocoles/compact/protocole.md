# Protocole compact - production d’une évolution par un agent LLM

## Ce que c'est

La méthode à suivre pour un **travail déjà cadré**, dont le résultat attendu est vérifiable
automatiquement. La conduite tient dans un document unique, `conduite_<theme>.md`.

Les cas et leurs attendus sont écrits avant l'implémentation, puis vérifiés par des contrôles
exécutables. La conduite conserve les sources, la surface d'écriture et les résultats.

Ce qui est réduit : **un document**, **aucun vérificateur dédié au protocole**, aucune instrumentation
probatoire. Les exigences de sourçage, de validation et de bornage restent dues.

**Ce que ce protocole ne fait pas.** Il ne dispense d'aucune revue et ne remplace aucun jugement
humain. Il rend vérifiable **ce qui a été vérifié** ; il ne dit pas que le travail est bon.

## Sa condition d'entrée

Le besoin, les limites du travail et les critères d'acceptation sont déjà établis dans le ticket
ou le document qui porte la demande. Pour le résultat principal, un attendu peut être fixé et
vérifié par un contrôle exécutable qui échouerait si ce résultat était incorrect.

**La condition d'entrée s'écrit.** La conduite cite le cadrage et nomme le contrôle, existant ou à
créer, avec son entrée, son attendu et sa condition d'échec. L'absence actuelle d'un test n'est pas
l'absence d'un oracle.

L'exécutant vérifie les sources et précise l'implémentation dans ce cadre. Si une décision nécessaire
dépasse le cadre établi, ou si aucun contrôle pertinent ne peut être défini, il rend la main.
Il ne choisit jamais sa méthode et n'en change pas en cours de route : le choix appartient au lanceur.

Si une acceptation dépend d'un jugement humain que les contrôles ne couvrent pas, l'exécutant
le signale et laisse cette acceptation en attente ; il ne la déclare pas acquise.

## Les cinq règles

Elles tiennent à chaque instant, et rien de ce qui suit ne les suspend.

- **R1 -- Le verdict ne vient jamais de l'agent.** Le résultat est validé par un oracle externe
  exécutable, dont le verdict se lit dans un artefact. Une relecture de son propre travail ne
  remplace pas cette validation.

- **R2 -- Aucune valeur n'est écrite si elle n'a pas été établie.** Ce que le code **est** se source
  sur le code ouvert et cité par son chemin absolu ; ce que le système **fait** se source sur une
  exécution observée ; ce qui est **exigé** se source sur ce qui fait autorité pour l'exiger. Lire
  ne suffit donc pas : une valeur de comportement trouvée dans une documentation n'est pas observée,
  et une exigence tirée du code n'est pas exigée. Un fait qu'aucune de ces trois voies n'établit
  s'écrit `ABSENT`, jamais sous la forme d'une valeur plausible assortie d'un conditionnel.

  Avant d’écrire, les valeurs, les décisions et les limites que l’écriture engage se relisent à leur
  source. Ni un souvenir ni un résumé de conversation n’en tient lieu. Ce qui manque se traite par
  les règles existantes d’inconnue et d’arrêt.

- **R3 -- L'écriture est bornée, et déclarée avant d'écrire.** Les fichiers que la conduite touchera
  sont énumérés dans le document de conduite, **et ce document est commité avant le premier
  changement de code**. Tout fichier absent de cette liste est en lecture seule.

- **R4 -- L'attendu est figé avant que le code existe.** Les cas de la conduite s'écrivent depuis le
  besoin, jamais depuis ce qui a été construit, et leur commit précède celui du code. C'est la seule
  garantie disponible contre le mode d'échec propre à ce travail : retoucher jusqu'à ce que le
  résultat ait l'air correct, puis oublier ce qu'on cherchait. **Un cas ne se retire ni ne
  s'assouplit parce qu'il vient d'échouer** ; il se corrige contre une raison écrite avant l'échec,
  ou la conduite s'arrête.

- **R5 -- Ce qui dépasse le cadre s'arrête.** Pas d'extension silencieuse du périmètre, pas de règle
  inventée en chemin. Un dépassement rend la main au propriétaire, l'état laissé tel quel.

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

## Ce que le projet doit fournir

**Une seule chose écrite d'avance : le régime d'autorisation**, dont le chemin est donné dans le
message qui ouvre la conduite. Tout le reste, l'agent le trouve en regardant et le consigne au pas 1.

La raison de cette asymétrie : une permission **ne se découvre pas, elle se donne**.

```markdown
| Décision | Valeur |
|---|---|
| Pré-autorisation des outils du CLI | <complète, par la commande exacte ; ou liste fermée ; ou aucune> |
| Création du ticket par l'agent | <autorisée, et où vit le mode d'emploi ; ou non autorisée> |
| Publication de la branche du sujet | <autorisée, et à quelles conditions ; ou non autorisée> |
| Branches principales du dépôt | <leurs noms exacts> |
| Convention de nommage des branches | <la convention, ou : celle de ce protocole> |
| Exceptions aux référentiels | <aucune ; ou la règle écartée, avec sa raison et sa date> |
```

**Absent, ou muet sur un point nécessaire, c'est un arrêt.** L'agent ne le complète pas lui-même :
il appartient au propriétaire du dépôt. Chaque décision porte sa date, et se retire en modifiant sa
ligne.

**Convention de branche par défaut**, quand le régime ne dit rien : `<type>/<sujet>`, le type pris
dans `feat`, `fix`, `docs`, `chore`.

## Les référentiels de conception et de codage

**Trois documents sont normatifs pour tout ce que la conduite écrit**, et se lisent en précondition,
**avant le pas 1** :

- `../../referentiels/conception.md` -- la conception ;
- `../../referentiels/conception_de_code_pour_llm.md` -- la conception LLM-friendly,
  parce que le LLM est l'outil d'assistance principal du développeur ;
- `../../referentiels/codage.md` -- le code écrit, les commentaires, le jeu de
  caractères, les conventions git, la documentation obligatoire.

Ils régissent aussi le document de la conduite, qui est le premier fichier écrit : les lire plus
tard reviendrait à ne les appliquer qu'ensuite. Ils ne se recopient pas et ne se résument pas -- un
résumé serait une seconde source, et un agent qui le lit croirait légitimement avoir tout lu.
`../../referentiels/conception.md` renvoie lui-même à `../../referentiels/gestion_des_erreurs.md`, et ce renvoi fait partie du
référentiel.

**Ce que le dépôt impose en plus reste dû** -- contrôle statique, style, typage.

Les références relatives de cette section se résolvent depuis le dossier de ce fichier de
protocole, jamais depuis le répertoire courant. Avant de les lire, les convertir en chemins absolus
et vérifier leur existence ; une référence introuvable est un arrêt.

## Le document unique

| Document | Ce qu'il porte |
|---|---|
| `conduite_<theme>.md` | La condition d'entrée établie, le départ, la surface d'écriture, les cas à éprouver, puis ce qui a été constaté |

Il vit dans le dossier que le dépôt réserve à ses notes de projet.

Le cadrage existant est cité, pas recopié. Les constats et précisions d'implémentation nécessaires
s'inscrivent dans les sections concernées de la conduite, sans document d'analyse ou de plan séparé.

## La marche à suivre

Cinq pas, dans cet ordre. Le commit initial de l'attendu et le commit final de validation encadrent
le travail ; aucun changement de code ne précède le commit initial.

| Pas | Ce qu'il écrit, et rien d'autre |
|---|---|
| 1. Ouvrir | rien encore -- il constate |
| 2. Fixer l'attendu | `conduite` : condition d'entrée, départ, surface, cas à éprouver. **Premier commit** |
| 3. Faire | les fichiers énumérés par la surface |
| 4. Éprouver | `conduite` : ce qui a été constaté. **Commit final de validation**, avec le code |
| 5. Clore | le référentiel du projet |

**1. Ouvrir.** Lire le régime d'autorisation ; absent ou muet, s'arrêter. Si la tâche est donnée par
un ticket, le lire avant de cadrer le travail et consigner son URL ainsi que sa date de consultation ;
s'il est inaccessible, s'arrêter. Si la branche courante est
l'une des branches principales déclarées par le régime d'autorisation, créer depuis son `HEAD` la
branche du sujet avec `git switch -c <nom conforme à la convention déclarée>`, vérifier qu'elle est
devenue la branche courante, puis continuer ; si la commande ou la vérification échoue, s'arrêter.
Vérifier que la branche courante est une branche du sujet. Relever le commit de départ, la commande
de validation du projet et son verdict. Vérifier le cadrage existant et identifier le contrôle
qui établira le résultat attendu.

Une validation de référence rouge est un arrêt, sauf si elle est rouge **parce qu'elle expose le
défaut traité** : c'est alors la preuve rouge, elle s'écrit, et la conduite continue.

**Amorçage sans validation initiale.** Si le projet ne possède encore aucune validation exécutable,
consigner `ABSENT` au départ et prévoir la création du premier contrôle dans la surface autorisée.
Son attendu est fixé avant l'implémentation du comportement contrôlé. À la clôture, exécuter la
validation ainsi créée : l'absence de validation initiale ne dispense pas de validation finale.
Si aucun contrôle pertinent ne peut être défini, rendre la main.

**2. Fixer l'attendu.** Écrire la conduite **depuis le besoin**, avant de modifier le code :
les cas à éprouver, leurs entrées, leurs attendus et les contrôles prévus, avec la liste des fichiers
à toucher. Commiter ce document **seul**. Ce commit prouve l'antériorité de l'attendu sur le code.

**3. Faire.** Appliquer le changement dans la seule surface déclarée. Écrire les contrôles prévus
dans la suite du projet. Chaque contrôle porte sur le résultat attendu ; une présence textuelle
ou une compilation réussie ne prouve pas à elle seule un comportement.

**Chaque contrôle écrit est falsifié avant d'être gardé.** Appliquer la mutation qu'il doit
attraper, le lancer seul, vérifier qu'il **rougit**, restaurer le fichier à l'octet près. Un
contrôle qu'on n'a pas vu rougir n'est pas un contrôle : c'est une assertion dont on suppose
qu'elle discrimine. La mutation appliquée et son résultat s'écrivent.

Une assertion toujours vraie peut passer la suite sans détecter le défaut : la falsification
vérifie que le contrôle discrimine le résultat incorrect.

**Un contrôle qui ne rougit sous aucune mutation se retire ou se refait** -- jamais il ne se
garde « au cas où ». Et quand une mutation qui **devait** le laisser vert le fait rougir, c'est
le contrôle qui est trop étroit : il attraperait des changements légitimes sans rien apprendre.

**4. Éprouver.** Exécuter les contrôles de chaque cas et consigner les résultats avec le chemin
de leurs artefacts, y compris les échecs. Lancer la validation du projet. Commiter le code et
la conduite remplie ensemble.

Un cas non éprouvé porte `NON EPROUVE` et sa raison. Il ne se laisse pas vide : une ligne vide est
indiscernable d'un oubli.

**5. Clore.** Verser dans le référentiel du projet ce que la conduite a appris, et **écrire ce qui
reste sans garantie**. Une conduite qui ne remonte rien l'écrit aussi : c'est un constat, pas un
silence.

## Le contrôle du protocole : Git

**Aucun contrôle mécanique dédié.** L'exécutant vérifie dans l'historique que l'attendu précède
le code et que les fichiers modifiés appartiennent à la surface déclarée. Cette commande fournit
les éléments à examiner ; elle ne rend pas de verdict de conformité :

```text
git log --reverse --name-only <commit de départ>..HEAD
```

Le premier commit ne doit porter que le document de conduite. Les commits suivants restent dans
la surface qu'il déclare. Le commit final de validation conserve le code et la conduite remplie.

Git conserve l'historique des changements ; la comparaison avec les exigences du protocole reste
à la charge de l'exécutant.

## Ce qui est appris ne meurt pas avec la conduite

La clôture verse dans **le référentiel du projet** -- celui relevé au pas 1 -- ce que la conduite a
appris. Une seule destination : ce protocole ne capitalise pas sur lui-même.

**Le seuil est fermé.** Ce qui est appris entre comme **observation**, datée. Cela devient une
**règle** à trois conditions cumulatives : réutilisabilité démontrée hors du cas qui l'a fait naître,
absence de règle équivalente déjà présente, confirmation sur un second contexte. À défaut, cela reste
une observation et se tranche à la consolidation suivante : promue ou retirée.

## Quand rendre la main

Ces situations ne se contournent pas et ne se traitent pas dans ce protocole. L'agent **s'arrête**,
écrit dans la conduite ce qu'il a constaté, et rend la main sans défaire ce qui est déjà commité.

| Situation | Pourquoi c'est un arrêt |
|---|---|
| Le régime d'autorisation est absent, ou muet sur un point nécessaire | Une permission ne se devine pas |
| Un référentiel déclaré est introuvable ou illisible | La conduite s'appuierait sur une règle qu'elle n'a pas lue |
| Après l'action prévue au pas 1, la branche courante n'est pas la branche du sujet | Le travail vit sur la branche du sujet, sans exception |
| Le cadrage nécessaire manque, ou aucun contrôle pertinent ne peut être défini | La condition d'entrée n'est pas remplie |
| Le changement ne produit pas l'effet attendu et la cause est inconnue | C'est une inconnue à observer, et observer n'est pas ce que fait ce protocole |
| Deux tentatives sur le même échec ont échoué | Au-delà, la correction devient de la recherche, et la surface se met à enfler |
| Un fichier hors de la surface déclarée doit être modifié | La surface est la garantie ; l'étendre en cours de route la supprime |
| Le travail toucherait la surface qui influence un modèle -- prompt, paramètres d'appel, forme des sorties d'outils | Cette surface se mesure avant adoption ; elle ne se juge pas à l'oeil |
| Une action non réversible, ou hors du périmètre déclaré, serait nécessaire | Elle appartient au propriétaire, pas à l'agent |

**Ce qui se passe après l'arrêt appartient à celui qui lance la conduite** : une autre méthode, une
autre découpe, un abandon. L'agent ne s'en saisit pas, et **ne convertit pas** ce qu'il a produit en
artefacts d'autre chose. Ce qui reprendra repartira de son propre premier pas.

Rendre la main n'est pas un échec de la conduite : c'est le cas nominal quand la tâche n'était pas
celle qu'on croyait. Le seul vrai défaut est de continuer sans le dire.

## Ce que l'agent fait avec l'historique

Il **ajoute de l'état récupérable**, et rien d'autre. Il n'en détruit aucun.

- Le commit initial de l'attendu et le commit final de validation sont obligatoires, dans cet ordre.
  Des commits intermédiaires sont permis entre les deux.
- **Sont interdits sans instruction explicite du propriétaire** : réécrire l'historique, supprimer ou
  déplacer de force une référence, fusionner vers une branche principale, abandonner des
  modifications non commitées.
- Publier dépend de la seule ligne du régime d'autorisation qui le dit.

## Le squelette

Recopier la structure en remplaçant les blocs entre chevrons. **Ne supprimer aucune section** : une
section sans objet porte la mention `Sans objet` et sa raison, une section vide est indiscernable
d'un oubli.

```text
# Conduite - <thème>

## 1. Condition d'entrée

- Cadrage établi : <source du besoin, des limites et des critères d'acceptation>
- Contrôle prévu : <contrôle existant ou à créer, entrée, attendu et condition d'échec>
- Établi en ouvrant ou en lançant : <fichiers ouverts, commandes lancées>

## 2. Départ

- Régime d'autorisation : <chemin absolu>, lu le <date>
- Source de la tâche : <besoin en clair, chemin absolu, ou URL HTTPS du ticket et date de consultation>
- Branche : <nom de la branche du sujet>
- Commit de départ : <identifiant du commit>
- Référentiel du projet où verser ce qui sera appris : <chemin absolu>
- Validation du projet : <commande exacte> -> <verdict>
- Ce que la tâche fait : <une à trois lignes>
- Ce qu'elle ne fait pas : <ce qui est volontairement laissé de côté>

## 3. Surface d'écriture

- <chemin absolu de ce document, toujours en première entrée>
- <un chemin absolu par ligne, tous écrits avant que le premier soit touché>

Tout fichier absent de cette liste est en lecture seule.

## 4. Cas à éprouver

| Cas et entrée | Attendu | Contrôle prévu |
|---|---|---|
| <cas et données d'entrée> | <résultat attendu> | <contrôle exécutable existant ou à créer> |

## 5. Contrôle mécanique écrit

<contrôles ajoutés ou réutilisés dans la suite du projet, avec leurs chemins absolus>

| Contrôle | Mutation appliquée | Résultat |
|---|---|---|
| <son nom> | <le changement exact qu'il doit attraper> | <rouge, et c'est ce qui est attendu ; ou : vert, et ce que le contrôle est devenu> |

## 6. Ce qui a été constaté

| Cas | Constat | Verdict |
|---|---|---|
| <l'intitulé du cas> | <résultat et chemin de l'artefact> | <conforme, écart, ou NON EPROUVE avec sa raison> |

- Validation du projet rejouée : <commande> -> <verdict>

## 7. Ce qui reste sans garantie

<ce que la conduite n'a pas couvert, et ce qu'aucun contrôle du dépôt n'établit ; ou : rien>
```

## Le message qui ouvre la conduite

```text
Applique le protocole spécifié ici :
  <chemin absolu de ce fichier protocole.md>

Le projet est décrit ici :
  <chemin absolu de la documentation du projet>

Le régime d'autorisation est ici :
  <chemin absolu du régime d'autorisation>

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

**Avant de lancer**, trois vérifications d'une minute : les chemins cités existent, le ticket éventuel
est accessible, et l'arbre de travail est propre.

## Ce que ce protocole ne garantit pas

- **Les contrôles ne prouvent que les propriétés qu'ils éprouvent.** Une acceptation humaine
  nécessaire et non obtenue reste en attente.
- **Les contrôles doivent être rejoués.** Leur présence dans la suite ne prouve pas qu'une
  modification ultérieure a été validée.

- **La surface d'écriture n'engage que par git.** Elle est visible après coup, jamais empêchée sur
  le moment.
- **La conformité aux trois référentiels n'est couverte par aucun contrôle.** Rien ne vérifie qu'ils
  ont été lus, ni qu'ils ont été suivis.
- **Il ne remplace pas la revue humaine.** Il rend le travail auditable ; il ne le certifie pas.
