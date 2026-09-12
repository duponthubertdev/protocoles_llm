# Protocole étendu - production d'une évolution par un agent LLM

## Ce que ce document est

La méthode de conduite d'une évolution d'un logiciel par un agent LLM travaillant en quasi-autonomie,
du périmètre fonctionnel jusqu'à la validation par exécution.

**Quasi-autonomie** veut dire une chose précise : l'agent décide et agit seul dans un périmètre
déclaré, et il s'arrête sur une liste fermée de cas. Ce n'est ni de l'autonomie -- il ne choisit ni
son périmètre ni le moment de publier -- ni de l'assistance -- il n'attend pas une validation humaine
entre deux actions.

Le document est **normatif et indépendant de toute technologie**. Il ne suppose ni langage, ni
framework, ni outillage particulier. Ce qu'un projet doit lui apporter vit dans un document séparé,
le **régime d'autorisation** du projet, décrit ci-dessous.

**Il est orienté vers l'exécution.** Il porte des règles, et les explications de mécanisme sans
lesquelles une règle s'applique de travers. Il ne porte ni historique, ni suivi de ses propres
applications, ni backlog. Une phrase qui ne sert ni à agir ni à appliquer correctement une règle
n'a pas sa place ici.

Il est organisé en trois parties, et l'ordre a un sens :

| Partie | Ce qu'elle porte | Quand elle s'applique |
|---|---|---|
| **I -- Les invariants** | Ce qui tient toujours : bornage de l'écriture, valeur observée, verdict externe, boucle de correction, cas d'arrêt, doctrine | **En permanence**, quelles que soient les phases exécutées |
| **II -- Le pipeline** | Les huit phases, de P0 à P7, et leurs artefacts | Quand une conduite s'ouvre |
| **III -- Documents et contrôles** | Formats imposés, règles de rédaction, contrôle déterministe | À chaque écriture et à chaque validation |

La partie I ne dépend pas de la partie II. C'est ce qui rend la quasi-autonomie possible : les
garanties ne viennent pas de la séquence, elles viennent des propriétés qui tiennent à chaque
instant.

## Ce que ce protocole ne fait pas

À lire avant de s'y fier, et non après.

- **Il ne dit rien de la pertinence fonctionnelle.** Il garantit qu'un livrable vérifie ce que le
  document dit qu'il vérifie ; il ne garantit pas que ce soit ce qu'il fallait vérifier.
- **Une prescription comportementale n'est pas une barrière.** Les règles de la boucle de correction
  déplacent une distribution de probabilité. Les seules barrières réelles sont le script, l'exécution
  et la lecture du diff par un humain.
- **Il ne dispense d'aucune revue.** Il rend le travail auditable à coût faible ; il ne remplace pas
  l'audit.
- **Il n'est pas un bac à sable.** Le régime d'autorisation et les manifestes sont déclaratifs : ils disent
  ce que l'agent doit toucher, ils ne l'en empêchent pas. Le contrôle statique est constatatif,
  postérieur aux actions.

## Ce que le projet doit fournir

**Presque rien, et c'est voulu.** Le protocole ne connaît ni chemin, ni commande, ni convention. Il
les obtient de deux façons, et une seule coûte au projet.

| Source | Ce qu'elle porte | Qui la produit |
|---|---|---|
| **Le relevé d'amorçage** | Ce que l'agent a **trouvé en regardant** : comment on lance, où se lit le verdict, quels canaux de preuve existent, ce que le contrôle statique ne couvre pas | **L'agent, en P0**, dans sa baseline |
| **Le régime d'autorisation** | Ce que le propriétaire a **décidé** : pré-autorisation du CLI, création du ticket, publication, et les exceptions aux règles par défaut du protocole | Le propriétaire, une fois, dans un fichier court et distinct |

### Le régime d'autorisation

C'est la seule chose que le protocole réclame d'écrit d'avance, parce que c'est la seule qui
**n'existe nulle part**. Une permission ne se découvre pas : elle se donne. Deux des trois décisions
ne sont même pas des documents -- la pré-autorisation est un drapeau de lancement de session.

**Il vit dans un fichier court et distinct**, et non dans la documentation du projet. La dépendance
va dans un seul sens : ce fichier cite la documentation du projet, jamais l'inverse. Une synthèse
d'architecture est lue par des agents qui font tout autre chose, et doit rester juste si ce protocole
n'est pas employé. Format et exemple : `gabarit_regime_dautorisation.md`. Une quinzaine de lignes.

**Un régime d'autorisation absent, ou muet sur un point nécessaire, est un arrêt** -- déclencheur
**E12**. L'agent ne le complète pas lui-même : il appartient au propriétaire du dépôt.

### Le relevé d'amorçage

**Tout le reste, l'agent le trouve.** Un projet n'a pas à pré-mâcher ce qu'une exploration établit,
et le pré-mâcher est même nuisible : un document qui répond d'avance à « comment on lance » devient
une **synthèse au second degré**, qui vieillit comme toute synthèse. Le protocole tranche déjà en
faveur du code contre la synthèse ; ajouter une synthèse de plus ajoute une source périmable.

Consigné en P0, sourcé, daté, attaché à une conduite : voir « P0 - Cadre et référence ».

### Les règles par défaut du protocole, et leurs exceptions

Le protocole porte des règles par défaut là où la variation entre projets n'apporte rien :

| Sujet | Règle par défaut |
|---|---|
| Nommage de la branche du sujet | `<type>/<numéro>-<sujet>`, type dans `feat`, `fix`, `docs`, `chore` |
| Préfixe de l'instrumentation probatoire | `releve`, dans la casse du projet -- `releve_` en souligné, `Releve` en capitales initiales |
| Les deux tables du contrat de correction | Fournies par ce document, en termes génériques |

**Un projet ne déclare que ce sur quoi la règle par défaut ne tient pas**, dans son régime d'autorisation, avec
la raison. C'est le cas quand l'historique d'un dépôt mêle plusieurs conventions de branche : l'agent
ne peut alors pas trancher à la place du propriétaire.

---

# Partie I -- Les invariants

Ce qui tient à chaque instant, indépendamment des phases exécutées.

## Le problème que ce protocole résout

Le problème n'est pas la capacité d'un agent à écrire du code. C'est la **variance** entre deux
exécutions du même travail, et la **dégradation silencieuse** quand une validation refuse de passer
au vert.

Trois défaillances :

- **La décision rejouée.** Les mêmes arbitrages sont repris à chaque évolution : niveau d'assertion,
  découpage, contrat des variantes. Chaque décision rejouée est un vecteur d'erreur.
- **La correction du code au lieu de la validation.** Après un échec, la complétion la plus probable
  est de modifier le code testé. L'étape de classification n'est pas un token probable : elle est
  sautée. Le code enfle d'attentes et de contournements, et devient parfois inutilisable.
- **La valeur plausible inventée.** Quand une valeur nécessaire est absente du contexte, le modèle
  produit la plus probable plutôt que de s'arrêter. Le résultat compile et échoue plus tard sans dire
  pourquoi.

Le protocole ne combat aucune des trois par de la bonne volonté. Il applique la hiérarchie des
leviers : déterminisme externe d'abord, structure ensuite, prescription comportementale fermée en
dernier recours, jamais de prose vertueuse.

## Les sept invariants

Ce sont des **propriétés du travail**, vérifiables à tout instant. Elles se distinguent de la
doctrine N1 à N11, qui répond d'avance à des arbitrages : un invariant décrit un état, une règle de
doctrine tranche un choix.

- **I1 -- Le verdict ne vient jamais de l'agent.** L'agent déclenche le contrôle et l'exécution ; ce
  qui ne doit pas venir de lui, c'est le jugement de réussite. La validation vient d'un oracle
  externe exécutable, même lorsque l'agent l'exécute lui-même. Un agent qui relit son propre travail
  valide ce qui ressemble à du travail structuré.
- **I2 -- Aucune valeur n'est écrite si elle n'a pas été observée.** Identifiants, valeurs attendues,
  signatures, versions, chemins : tout provient d'un fichier lu ou d'une observation, cité par son
  chemin absolu. En l'absence d'observation, on écrit que l'observation manque.
  Avant d’écrire, les valeurs, les décisions et les limites que l’écriture engage se relisent à leur
  source. Ni un souvenir ni un résumé de conversation n’en tient lieu. Ce qui manque se traite par
  les règles existantes d’inconnue et d’arrêt.
- **I3 -- L'écriture est bornée à chaque instant.** À tout moment, l'ensemble des fichiers
  modifiables est fini et énuméré. Dans cet ensemble, l'agent agit sans demander d'autorisation ;
  hors de cet ensemble, il s'arrête. Demander la permission d'une action déjà autorisée n'ajoute
  aucune sûreté : cela renvoie à l'humain une décision que le périmètre a déjà tranchée, et brouille
  le signal d'un arrêt véritable.
- **I4 -- Un échec est une information.** Une validation rouge qui décrit correctement le
  comportement attendu est un succès du protocole, même si elle reste rouge.
- **I5 -- Toute sortie porte des critères observables et laisse une trace de la décision.** Le
  protocole ferme ce qu'il peut fermer, mais il n'élimine pas le jugement : décider si deux cas sont
  deux facettes d'un même parcours, si une abstraction est justifiée, si un effet reste cohérent avec
  l'intention métier, ou si une pratique est mûre, demande une appréciation. Ces jugements sont
  encadrés et tracés, pas supprimés. Prétendre le contraire donnerait une fausse assurance.
- **I6 -- Les référentiels sont nourris, pas seulement consommés.** Ce qu'une évolution apprend à ses
  dépens doit épargner l'apprentissage à la suivante. Le mécanisme est en P7 ; N9 en fixe le critère
  de maturité.
- **I7 -- Une contradiction documentaire est fatale.** Un agent froid ne réconcilie pas deux
  documents incompatibles : il suit le dernier lu, ou fabrique une synthèse qui ne respecte ni l'un
  ni l'autre. Un seul fichier fait foi pour un sujet donné.

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

## Ce que l'agent fait avec git

**L'agent commite et publie sa branche derrière une porte mécanique. Il ne détruit rien et n'engage
rien.** La frontière n'est pas « git » mais la distinction entre ce qui ajoute de l'état récupérable,
ce qui en détruit, et ce qui engage le dépôt vis-à-vis d'autrui.

| Catégorie | Opérations | Régime |
|---|---|---|
| **Lecture** | `git status`, `git diff`, `git log`, `git show`, `git branch --list` | Libre, en toute phase |
| **Ajout** | `git switch -c <branche du sujet>`, `git add <chemins explicites>`, `git commit` | **Autorisé sans demander**, sur la branche du sujet uniquement |
| **Destruction** | `git reset --hard`, `git checkout -- <fichier>`, `git restore` sans `--staged`, `git clean`, `git stash drop`, `git stash clear`, `git commit --amend`, `git rebase`, `git branch -d` et `-D`, toute réécriture d'historique | **Interdit, sans exception.** L'agent s'arrête et expose le besoin -- déclencheur **E11** |
| **Publication de la branche du sujet** | `git push` de la branche du sujet, sans `--force` | **Autorisé, une fois la porte de publication franchie.** Voir ci-dessous |
| **Publication engageante** | `git push --force` et toute variante, `git push` d'une branche principale, suppression d'une branche distante, ouverture d'une demande de fusion, fusion | **Réservé au propriétaire du dépôt** -- déclencheur **E11** |

Ce protocole s'appuie sur un filet : l'arbre de travail rend récupérables les modifications des
fichiers **suivis**. Les opérations d'ajout **construisent** ce filet, celles de destruction le
détruisent -- d'où la découpe, plutôt qu'un refus global.

Le filet ne couvre ni les fichiers non suivis ou ignorés, ni les ressources extérieures au dépôt, ni
l'environnement d'exécution. La frontière n'est d'ailleurs pas le commit mais le suivi : un commit
reste rattrapable, alors qu'un artefact jamais indexé disparaît sans recours **par git**. La branche
dédiée isole l'historique, elle n'isole pas les effets.

### La porte de publication

**L'agent publie sa branche quand une porte mécanique l'y autorise, jamais parce qu'il estime que
tout s'est bien passé.** La distinction n'est pas rhétorique : un agent qui juge son propre travail
le juge avec l'appareil qui vient éventuellement de se tromper. C'est l'invariant **I1** -- le
verdict ne vient jamais de l'agent -- appliqué à la dernière opération de la conduite.

La commande est celle du contrôle statique du projet, relevée en P0. Code `0` : la branche peut être poussée. Tout autre code : elle ne
peut pas, et l'agent expose le constat.

La porte vérifie quatre choses, en plus de tous les contrôles statiques habituels :

1. **la branche est celle du sujet** : ni un `HEAD` détaché, ni une branche principale, un nom
   conforme à la convention de nommage de branche, **et l'égalité avec la clé `branche_du_sujet` du manifeste,
   obligatoire pour publier**. La convention prouve la *forme* d'une branche de sujet ; elle ne
   prouve jamais qu'il s'agit de la branche de **ce** ticket ;
2. **le périmètre déclaré est entièrement commité** ;
3. aucun fichier non suivi ne subsiste sous le dossier du chantier ni sous un chemin déclaré ;
4. **chaque fiche des notes d'exécution porte un statut, et aucune n'est `OUVERTE`.** Une fiche
   muette sur son statut est un manquement au même titre qu'une fiche ouverte : sans cela, une fiche
   rédigée autrement passerait pour close.

**Le critère est « le périmètre est propre », et non « l'arbre de travail est propre ».** Exiger un
arbre entièrement propre bloquerait l'agent pour des fichiers qui ne le concernent pas -- le travail
non suivi d'un autre chantier, par exemple. Le risque réel est de publier un état qui ne correspond
pas à ce qui a été validé, et ce risque ne porte que sur le périmètre déclaré.

Conséquence directe sur l'autonomie, et c'est l'intention :

| Ce que la porte refuse | Ce que l'agent fait |
|---|---|
| Un fichier du périmètre n'est pas commité | Il le commite -- c'est une opération d'ajout, déjà autorisée -- et rejoue la porte. **Sans demander** |
| Un fichier suivi **hors** périmètre est modifié | Il s'arrête et expose : il ne peut pas savoir si ce fichier est à lui. C'est déjà un cas d'arrêt E6 |
| Une fiche d'exécution est restée ouverte | Il s'arrête : publier un travail que son propre auteur déclare non tranché n'aurait pas de sens |

**Ce que la porte ne fait pas, et qu'il ne faut pas lui prêter.**

- Elle n'atteste pas que les validations par exécution ont eu lieu. Elle ne remplace pas la
  definition of done, qui reste la condition d'entrée en P7 ; la porte s'y ajoute.
- Elle n'atteste pas que **tous les commits de la branche** appartiennent au périmètre déclaré. Elle
  lit l'index et l'arbre de travail, jamais l'historique -- et elle ne peut pas faire autrement : le
  manifeste ne déclare que ce que le contrôle statique doit inspecter, alors qu'une conduite touche
  légitimement des abstractions partagées qu'aucune clé ne couvre, et les référentiels que P7 doit
  alimenter. Comparer l'historique au manifeste refuserait une conduite parfaitement conforme.

La revue du contenu de la branche reste donc humaine, et elle a son moment : l'ouverture de la
demande de fusion, réservée au propriétaire du dépôt. Publier une branche de sujet ne la **fusionne**
pas.

**Mais un push n'est pas sans effet extérieur.** Il peut déclencher une intégration continue, des
crochets serveur, des notifications. C'est une publication distante, pas une simple sauvegarde, et
c'est pourquoi elle reste conditionnée à une porte plutôt que libre.

### Quand reprendre cette porte

Elle n'est pas parfaite et ne cherche pas à l'être. Elle se reprend dans trois cas, et pas sur une
impression :

- elle produit un **faux vert ou un faux rouge en usage réel** ;
- **sa promesse change** -- si l'on veut lui faire attester davantage que l'état local ;
- **le format du manifeste évolue**, puisqu'elle en dépend.

Attester l'historique complet d'une branche demanderait une **seconde surface déclarative**,
distincte de la surface d'inspection statique, avec ses propres tests. C'est un chantier à part
entière, pas un durcissement de celle-ci.

**La porte constate un état, à un instant.** Un commit ajouté après elle serait poussé sans avoir été
contrôlé. Elle affiche donc le **SHA autorisé**, et la règle est fermée : ce SHA doit encore être
`HEAD` au moment du `git push`. S'il ne l'est plus, la porte se rejoue. Un contrôle en amont d'une
action ne garantit jamais l'action elle-même ; nommer l'objet contrôlé est ce qui rend l'écart
détectable.

**Ce qu'un push ne défait pas.** Une branche publiée ne se retire que par une opération de
destruction, qui est interdite à l'agent. Ce qui est poussé est poussé -- y compris un artefact non
voulu, que la porte ne détecte pas. Le gain qui justifie ce risque n'est pas l'autonomie mais la
**sauvegarde** : sans publication, le travail d'une conduite n'existe que sur un poste.

### Points de commit obligatoires

1. **Un commit de référence** avant la première exécution d'une phase qui écrit du code.
2. **Un commit par correction** dans la boucle de correction, dont le message porte la classe du KO.
3. **L'instrumentation probatoire, avant son retrait** -- règle S8.
4. **L'artefact de chaque phase, à la clôture de cette phase.** Une phase dont l'artefact n'est pas
   commité n'est pas terminée.

Ils rendent possible un contrôle indépendant et peu coûteux : comparer l'ordre des commits aux
horodatages des artefacts d'exécution.

### Interdits qui bornent l'ajout

Une opération peut être de la catégorie « ajout » et rester interdite sous cette forme.

- **`git add -A` et `git add .`** : seuls des chemins explicites sont indexés. La surface d'écriture
  déclarée est la frontière, et une indexation globale y ferait entrer des fichiers qu'aucune phase
  n'a déclarés.
- **Aucun commit sur la branche principale**, jamais. Son nom est relevé en P0. P0 s'arrête déjà si
  elle est la branche courante.
- **Aucune suppression de la branche du sujet**, même après fusion : cette décision appartient au
  propriétaire du dépôt, qui peut aussi retirer toute cette autorisation en le déclarant -- S8 porte
  alors la conduite de repli.
- **Aucun `git push` avant la porte de publication**, et jamais depuis une branche principale. La
  porte se franchit une fois, en fin de conduite ; elle ne se rejoue pas après chaque commit.

### Limite, à connaître avant de s'y fier

**Un commit prouve une séquence, pas une honnêteté.** Les messages sont écrits par l'agent. Le
contrôle par comparaison aux horodatages des artefacts reste extérieur, et reste nécessaire.

## Déclencheurs d'escalade

Liste fermée. En dehors de ces cas, l'agent décide seul dans le périmètre de la doctrine. Dans ces
cas, il s'arrête, écrit le constat, et attend une décision.

| Code | Déclencheur |
|---|---|
| E1 | Une anomalie de la source d'exigences touche le périmètre traité. |
| E2 | Un cas d'utilisation n'est pas spécifié, ou l'est de façon non exécutable. |
| E3 | Aucune donnée productible ne permet d'exercer le comportement à vérifier. |
| E4 | L'environnement, un compte ou un droit nécessaire n'est pas disponible. |
| E5 | L'action ne produit aucun effet observable, ou l'effet observé contredit l'intention métier. Une simple imprécision de rédaction du cas d'utilisation n'est pas un déclencheur. |
| E6 | Corriger un échec imposerait de modifier un fichier hors du périmètre autorisé. |
| E7 | Une décision nécessaire contredit un choix déjà livré par une évolution antérieure. |
| E8 | Deux tentatives de correction sur le même symptôme ont échoué. |
| E9 | Une observation nécessaire est impossible à obtenir, y compris la preuve rouge préalable d'une anomalie. |
| E10 | Une validation paraît elle-même fausse. |
| E11 | Poursuivre exigerait une opération git de destruction, ou une publication engageante -- `--force`, branche principale, suppression distante, demande de fusion. La publication de la branche du sujet n'est pas un déclencheur : elle a sa porte. |
| E12 | Le régime d'autorisation du projet est absent, ou muet sur un point nécessaire à la conduite. |

### Portée d'un arrêt

**La portée d'un arrêt est celle de ce que le déclencheur bloque, et rien de plus.** Le défaut est la
portée la plus étroite qui rétablisse la cohérence.

| Portée | Quand | Ce qui continue |
|---|---|---|
| **La ligne concernée** -- cas par défaut | E1, E2, E3, E5, E6, E7, E8, E9, E10 ; **E4 quand l'indisponibilité est propre à cette ligne** | tout le reste du périmètre |
| **L'opération concernée seule** | **E11 quand l'opération git est isolable** et ne conditionne pas la suite | tout le reste |
| **La conduite entière** | **E4 quand l'indisponibilité est globale** ; **E11 quand l'opération conditionne la suite** ; **E12 quand la décision manquante conditionne la conduite entière** | rien : l'agent expose le constat et attend |

**E4, E11 et E12 ont une portée conditionnelle ; les neuf autres ont une portée fixe.** Leur portée
ne se lit pas dans le code, mais dans le constat. Un régime d'autorisation muet sur la publication n'arrête
que la publication ; muet sur la pré-autorisation, il arrête tout.

**Élargir un arrêt au-delà de ce que le déclencheur bloque est une faute symétrique de celle de
poursuivre malgré lui.** Bloquer tout un périmètre au premier obstacle est la plus coûteuse des deux,
parce qu'elle se présente comme de la prudence.

Dans tous les cas, le document final dit explicitement ce qui a été livré et ce qui ne l'a pas été.

**Un arrêt n'est pas un échec de l'agent.** C'est le comportement attendu, et il est préférable à une
correction hasardeuse. Cette phrase doit figurer dans le document portant le contrat de correction :
sans elle, un agent qui veut bien faire s'obstine, et l'obstination est exactement ce que ce
protocole cherche à empêcher.

## La boucle de correction encadrée

C'est la partie du protocole qui traite la défaillance la plus coûteuse : corriger le code alors que
c'est la validation qui a tort.

Elle se lit en deux temps. **La doctrine ci-dessous explique pourquoi le dispositif est ce qu'il
est** : elle sert à le maintenir, et elle ne se recopie pas. **Le bloc canonique, plus bas, est le
contrat opérationnel** : il dit quoi faire au moment d'un échec, et il se recopie tel quel.

### Pourquoi le contrat est recopié, et non simplement référencé

L'exécutant ne doit jamais avoir à ouvrir le présent document pour savoir quoi faire après un échec.
Un document qui l'y oblige est incomplet : au moment précis où l'improvisation est la plus tentante,
la conduite à tenir doit être sous les yeux.

**Une conduite partielle produit et exécute quand même.** Une mesure, une observation, une
investigation ne livrent aucun code et n'ont donc pas de P5 ni de P6. Elles agissent pourtant : elles
écrivent de l'instrumentation et lancent des exécutions, donc elles peuvent échouer. Rattacher le
contrat au seul plan le retirait précisément aux conduites qui s'arrêtent avant lui.

### Quel document porte le contrat, et quand

Le **plan d'implémentation** quand la conduite en produit un, le **cadrage** sinon. C'est celui que le
manifeste déclare sous `contrat_de_correction`, et celui où vit la section « Notes d'exécution ».

Le critère n'est pas « la conduite aura-t-elle un plan ? » mais **« agit-elle avant que le plan
existe ? »**. Une conduite agit dès qu'elle écrit de l'instrumentation et lance une exécution,
c'est-à-dire dès P3. Le cadrage porte donc le contrat tant que le plan n'existe pas, puis le plan le
porte à son tour ; le manifeste suit.

### Ce que la doctrine ajoute au bloc

Ces explications éclairent le bloc sans y figurer. Les recopier obligerait l'exécutant à trier ce qui
le concerne au moment où il doit agir.

**Sur la distinction entre l'action mal exécutée et l'échec réel.** Sans elle, l'exécutant écrit des
fiches pour des fautes de frappe, puis cesse d'en écrire du tout.

**Sur la fiche écrite avant toute écriture.** C'est la seule façon de rendre la question observable.
Une règle qui demanderait seulement de « se poser la question » ne laisserait aucune trace, donc
aucune possibilité d'audit. Et c'est une contrainte de chronologie, pas un détail d'emplacement : une
conduite partielle peut échouer dès P3, alors que l'analyse détaillée n'existe qu'en P4. Loger les
fiches dans l'analyse laisserait l'agent sans endroit où écrire au moment précis où la règle lui
interdit d'ouvrir un fichier avant de l'avoir fait.

**Sur le périmètre gelé.** Le critère est la déclaration, pas l'ancienneté du fichier. Une évolution
dont l'objet est justement de modifier un fichier existant doit pouvoir le corriger ; les geler par
principe rendrait le protocole applicable aux seules créations.

**Sur la classe « validation fausse ».** Elle n'est pas facultative. Un défaut peut n'être ni dans la
donnée, ni dans le code, ni dans l'application, mais dans le critère de succès lui-même. Sans classe
dédiée, la tentation d'y voir un simple ajustement technique augmente.

**Sur l'autorisation d'instrumenter.** Sans elle, le protocole interdirait d'observer au moment
précis où c'est le plus utile, ce qui pousserait à corriger à l'aveugle.

**Sur le plafond de deux tentatives.** La conviction après deux échecs est le signal le moins fiable
disponible : les causes secondaires étant éliminées, les hypothèses restantes convergent vers la plus
probable, qui n'est pas nécessairement la vraie.

**Sur le vocabulaire de la variation.** Le mot **intermittence** est réservé au résultat d'une
mesure : une fréquence et des conditions établies. Avant cette mesure, on parle de **contradiction**.
Un échec suivi d'un succès établit qu'il y a quelque chose à investiguer, rien de plus.

### Le bloc canonique, et sa règle de recopie

Le bloc délimité ci-dessous est **le contrat opérationnel**. Il est entièrement générique : il ne
nomme ni le cadrage ni le plan, ne porte aucun code de déclencheur d'escalade, et ne contient rien à
substituer ni à adapter.

**Il se recopie tel quel, sans reformulation, sans ajout et sans retrait**, entre ses deux marqueurs
de délimitation exclus. Les deux gabarits l'exigent, et le contrôle statique cherche ses marqueurs
dans le document que le manifeste déclare.

**Adapter le bloc à un chantier est interdit.** Ce qui est propre à une conduite -- la liste de ses
fichiers, ses validations, ses artefacts -- vit dans le document qui l'accueille, autour du bloc,
jamais dedans.

**Pourquoi la recopie doit être mécanique.** « Recopier la section » demandait à l'agent de **juger**
ce qui relevait du contrat, sur une section qui mêlait doctrine et mode opératoire. Le protocole dit
lui-même qu'une convention exigeant du jugement produit de la variance. Entre deux marqueurs, la
recopie est mécanique, donc comparable.

<!-- CONTRAT DE CORRECTION : DEBUT -->

## Conduite à tenir quand une validation échoue

**Un arrêt n'est pas un échec de l'exécutant.** C'est le comportement attendu, et il est préférable à
une correction hasardeuse. Un agent qui veut bien faire peut s'obstiner, et l'obstination est
exactement ce que ce dispositif cherche à empêcher.

### Deux situations à ne pas confondre

**L'action n'a pas été exécutée comme écrite.** Fichier oublié, contenu tronqué, faute de frappe. On
refait l'action et on relance la validation. Ce n'est pas un échec, et cela ne demande aucune fiche.

**L'action a été exécutée comme écrite et la validation échoue quand même.** C'est un échec réel, et
il déclenche intégralement la procédure ci-dessous.

### La fiche s'écrit avant toute écriture

Avant toute écriture consécutive à un échec réel, écrire une fiche dans la
section « Notes d'exécution » du document portant le contrat, au format fixé par le gabarit de plan
d'implémentation. La fiche répond à :

> Le comportement observé est-il conforme à ce que le cas d'utilisation décrit ?

| Constat | Qui a tort | Conséquence |
|---|---|---|
| Le système produit un résultat cohérent avec l'intention, l'attendu de la validation est absent ou différent | La validation | Corriger l'attendu |
| L'effet produit est observable, mais diffère de la lettre du cas d'utilisation | La rédaction du cas d'utilisation | Ajuster l'oracle à l'effet réel et documenter l'écart |
| Aucun effet observable, ou effet contraire à l'intention métier | Le comportement applicatif | **Arrêt, aucune correction** |
| Le dispositif ne trouve pas ce qu'une observation prouve présent | La désignation employée -- sélecteur, chemin, clé, identifiant | Corriger la désignation, après nouvelle observation |
| Le dispositif fait autre chose que ce que le scénario décrit | Le scénario | Corriger le scénario |
| La donnée nécessaire n'a jamais été produite | Le producteur de la donnée | Corriger le producteur, ou **arrêt** |
| Un résultat varie sans qu'aucune modification l'explique | Rien n'est établi | **Se mesure, ne se corrige pas** |

La frontière entre « la rédaction a tort » et « le comportement applicatif a tort » est l'existence
d'un **effet observable**. Un cas d'utilisation est une description humaine, jamais parfaite : un
écart de forme s'absorbe en ajustant l'oracle. Seule l'absence d'effet, ou un effet contraire à
l'intention métier, bloque.

### Surface d'écriture autorisée

Pendant la correction, la surface est **celle qu'a déclarée le document portant le contrat**, ni plus
ni moins. Un fichier préexistant que ce document autorise à modifier reste modifiable ; un fichier
qu'il n'a pas déclaré est en lecture seule, même s'il a été créé par la conduite.

| Classe du KO | Surface autorisée, dans les limites du périmètre déclaré |
|---|---|
| Attendu faux | L'artefact qui porte l'attendu |
| Désignation fausse | L'artefact qui porte la désignation, après nouvelle observation |
| Scénario faux | L'artefact qui porte le scénario |
| Production mal construite | L'artefact qui décrit la production de la donnée |
| Donnée absente ou producteur en échec | Aucune -- arrêt |
| Comportement applicatif divergent | Aucune -- arrêt |
| Défaut hors périmètre déclaré | Aucune -- arrêt |
| Validation fausse | Aucune -- arrêt |
| Variation inexpliquée | Aucune -- à mesurer séparément |

La classe du KO restreint la **nature** du fichier modifiable ; le périmètre déclaré en restreint la
**liste**. Les deux s'appliquent.

### Les interdits

- aucune attente ajoutée qui ne soit une intention nommée adossée à un témoin déclaré ;
- aucune reprise locale, aucune pause fixe, aucune action par contournement technique, aucune action
  par index ;
- aucune extension d'une abstraction existante pour absorber un cas particulier.

Un quatrième prime sur les trois autres : **ne jamais modifier une validation pour la faire passer.**
Un agent bloqué peut toujours affaiblir son propre critère de succès, et c'est la sortie la plus
tentante puisqu'elle réussit à coup sûr. Une validation affaiblie transforme un échec bruyant en faux
vert silencieux.

Si une validation paraît elle-même fausse, c'est un cas d'arrêt, pas une invitation à la corriger.

### Instrumenter reste autorisé

La table des surfaces borne les **corrections**. Elle ne borne pas l'observation : un agent bloqué a
le droit de poser une instrumentation de diagnostic temporaire, y compris en créant un artefact neuf,
quelle que soit la classe du KO.

Conditions : l'artefact porte le préfixe `releve` ; sa règle de retrait est écrite avant son code ;
il ne porte aucune assertion et ne corrige rien ; il ne compte pas dans le plafond.

### Le plafond

**Deux tentatives sur le même symptôme.** À la troisième, arrêt, quel que soit le niveau de
conviction.

### Cas d'arrêt immédiat

L'agent s'arrête, écrit le constat avec ses preuves, et attend une décision.

- une anomalie de la source d'exigences touche le périmètre traité ;
- un cas d'utilisation n'est pas spécifié, ou l'est de façon non exécutable ;
- aucune donnée productible ne permet d'exercer le comportement à vérifier ;
- l'environnement, un compte ou un droit nécessaire n'est pas disponible ;
- l'action ne produit aucun effet observable, ou l'effet observé contredit l'intention métier -- une
  simple imprécision de rédaction du cas d'utilisation n'est pas un cas d'arrêt ;
- corriger un échec imposerait de modifier un fichier hors du périmètre autorisé ;
- une décision nécessaire contredit un choix déjà livré antérieurement ;
- deux tentatives de correction sur le même symptôme ont échoué ;
- une observation nécessaire est impossible à obtenir ;
- une validation paraît elle-même fausse ;
- poursuivre exigerait une opération de destruction ou une publication engageante ;
- le régime d'autorisation du dépôt est absent, ou ne tranche pas une autorisation nécessaire à la poursuite.

**La portée d'un arrêt est celle de ce qu'il bloque, et rien de plus.** Par défaut c'est la ligne
concernée, et tout le reste du périmètre continue. Élargir un arrêt au-delà de ce qu'il bloque est
une faute symétrique de celle de poursuivre malgré lui : bloquer tout un périmètre au premier
obstacle se présente comme de la prudence, et coûte plus cher.

Dans tous les cas, le document final dit explicitement ce qui a été livré et ce qui ne l'a pas été.

### Une variation inexpliquée se mesure

Un symptôme qui apparaît puis disparaît sans qu'aucune modification l'explique n'entre dans aucune
ligne de la table des surfaces. Il arrête **la ligne concernée, jamais la conduite**, et se classe
avec, au minimum : les deux populations d'observations contradictoires et le nombre de passages de
chacune, la preuve que le code et les données étaient identiques entre elles, et le constat qu'aucune
correction opportuniste n'a été appliquée entre-temps.

La mesure devient un travail distinct, proposé et non exécuté.

### Reprise après un arrêt

Un arrêt n'est pas une fin. Le chemin est le même pour tous les cas d'arrêt.

1. Écrire la fiche, s'arrêter, et exposer le constat avec ses preuves et, s'il y en a une, la
   correction proposée **sans l'appliquer**.
2. Le propriétaire du dépôt décide : correction validée, autre approche, ou abandon de la ligne.
3. Si la correction est validée, l'appliquer. La lacune qui a conduit à l'arrêt reste consignée dans
   la fiche ; le propriétaire décide si elle justifie une évolution du protocole. Une faute ponctuelle
   dans un script ne justifie pas une règle générale.
4. **Reprendre à l'étape minimale suffisante, jamais depuis le début.** Corriger une validation
   reprend à cette validation seule ; corriger une valeur observée reprend à l'observation qui l'a
   produite ; corriger une décision de conception reprend à l'analyse.
5. Clore la fiche par son résultat.

<!-- CONTRAT DE CORRECTION : FIN -->

### La reprise minimale a une conséquence de conception

Elle est énoncée dans le gabarit de plan : une validation qui exécute elle-même l'action ne peut pas
être rejouée seule, et impose de tout réexécuter pour corriger un simple critère. Séparer le
déclenchement du constat rend la reprise minimale possible.

### Le filet

Une granularité de commit fine est le filet le plus efficace : elle permet un retour en arrière
chirurgical plutôt qu'un abandon complet. Elle est **obligatoire**, et ses points sont énumérés dans
« Ce que l'agent fait avec git ».

Les notes d'exécution restent la contrepartie documentaire. Elles ne se substituent pas aux commits :
un commit porte une date et un contenu vérifiables, une note porte une narration.

## L'instrumentation probatoire temporaire

### Pourquoi une instrumentation plutôt qu'une observation manuelle

Une observation manuelle n'est ni reproductible, ni archivée, ni prise dans l'état exact où le
système travaille. Une instrumentation exécutée comme une exécution normale donne les trois. Elle
transforme l'observation en artefact versionné, ce qui rend possible un contrôle déterministe : une
valeur employée dans le code livré doit apparaître dans une observation.

### Règles

- **S1** C'est une mutation de diagnostic temporaire. Sa règle de retrait est écrite avant son code.
- **S2** Elle ne porte aucune assertion et ne modifie rien au-delà de ce que sa séquence prévoit
  déjà.
- **S3** Elle écrit ses relevés dans le dossier du chantier, pour qu'ils survivent à l'exécution et à
  la session. Une passe qui la rejoue n'écrase pas les preuves de la précédente : ce qu'une passe a
  établi peut ne plus être reproductible à la suivante.
- **S4** Son nom porte le préfixe `releve`, dans la casse du projet, ce qui rend son oubli
  détectable par script.
- **S5** Aucune valeur n'entre dans le code livré si elle n'apparaît pas dans une observation.
- **S6** L'ordre des observations est une décision de conception, écrite avant le code. Pour chaque
  observation, déclarer l'état qu'elle exige et les actions qui le détruisent. Toute observation
  précède la première action qui détruit son état, ou vit dans un parcours qui le reconstruit. Une
  instrumentation portant plusieurs actions mutantes reconstruit l'état entre elles, ou les répartit
  sur plusieurs séquences.
- **S7** Une instrumentation qui mesure ce qu'un livrable mesurera emploie le **même critère de
  stabilisation** que lui. À défaut, les deux ne mesurent pas la même chose, et l'instrumentation
  conclut à une absence là où le livrable verra une présence.
- **S8** Une instrumentation est **commitée avant d'être retirée**. Le commit est ce qui rend la
  règle de retrait réversible ; sans lui, le retrait est une destruction. Dans un dépôt qui retire à
  l'agent l'autorisation de commiter, la règle de retrait **ne s'exécute pas** tant que le
  propriétaire n'a pas commité l'artefact : l'agent le lui demande et attend.

**Pourquoi S1 et S4 comptent.** Une instrumentation oubliée n'est pas un fichier mort. Selon le
mécanisme de chargement du projet, elle peut être découverte, instanciée, et entrer en collision avec
un artefact livré. Le relevé d'amorçage décrit ce mécanisme quand il existe ; le protocole se contente d'en tirer la
conséquence : la règle de retrait et le préfixe détectable bornent ce coût, et sans eux il n'est pas
borné.

S6 et S7 traitent l'instrumentation comme ce qu'elle est : non un artefact mais un programme, avec
ses préconditions et ses effets destructifs.

Une instrumentation déjà écrite se récupère depuis l'historique plutôt que de se conserver dans le
code livré, **sous réserve que S8 ait été respectée**.

**Une recherche vide n'établit rien.** C'est le piège, et il est coûteux. Un gestionnaire de versions
peut **élaguer** l'historique d'un chemin resté inchangé au net d'un commit de fusion : un artefact
créé puis supprimé dans une branche déjà fusionnée -- c'est-à-dire l'état normal de toute
instrumentation passée -- devient alors introuvable par une recherche ordinaire. Mesuré sur un dépôt
réel : **zéro commit trouvé sans l'option d'historique complet, quinze avec**, alors que le premier
d'entre eux était ancêtre de la branche principale.

Conclure d'une sortie vide que l'artefact n'a jamais été commité fait réécrire ce qui existait. Sur
le cas mesuré, mille trois cents lignes et six corrections auraient été perdues.

```powershell
git log --oneline --all --full-history --diff-filter=ACMRT -- "**/<prefixe>*"
git show <commit>:<chemin> > <destination>
```

**Sélectionner le résultat le plus récent où le fichier existe** : les versions antérieures peuvent
porter des défauts que les passes suivantes ont corrigés. Et si la recherche reste vide **avec**
l'option d'historique complet, alors seulement l'artefact n'existe pas.

Il faudra de toute façon l'adapter : une instrumentation utile est ciblée sur le symptôme constaté,
pas générique. C'est pourquoi on n'en conserve pas dans le code livré « au cas où » -- ce qui se
conserve est la méthode, pas l'artefact.

## Doctrine des décisions par défaut

Ces règles répondent d'avance aux arbitrages qui se répètent d'une évolution à l'autre. Elles sont
fermées : elles s'appliquent sans jugement. Une règle qui ne convient pas se corrige ici, avec
l'accord du propriétaire ; elle ne se contourne pas localement.

Le protocole ne porte que les règles **valables quelle que soit la technologie**. Tout le reste appartient à la doctrine du projet, et vit dans sa synthèse.

- **N1 -- Valeur exacte par défaut.** Toute valeur observable dont l'attendu est dérivable d'une
  donnée maîtrisée est vérifiée en valeur exacte. La vérification de présence seule est réservée aux
  valeurs non maîtrisables, et le document doit nommer la raison précise de la non-maîtrise.
- **N2 -- Un oracle ne réussit pas à vide.** Un oracle qui peut réussir alors que le comportement
  vérifié n'a pas eu lieu est interdit. En particulier, une attente qui réussit quand son témoin est
  absent transforme un échec bruyant en faux vert silencieux.
- **N3 -- Une absence se prouve sur un état prouvé.** Une vérification négative doit d'abord établir
  que le système est dans l'état attendu. Sans cette preuve, l'absence ne démontre rien.
- **N4 -- Conventions relevées, jamais inventées.** Ne pas inventer une convention nouvelle pour une
  évolution. En P0, relever la **convention normative applicable** -- référentiel imposé, puis règle
  propre au projet --, ses **exceptions déclarées** dans le régime d'autorisation, et la **conformité
  du code observé**. Les noms suivent la convention ainsi établie, et non le premier usage rencontré.

  **Une divergence non déclarée est un écart, pas une convention locale.** Le code observé décrit un
  état, il ne fait pas règle : une divergence peut être une dette autant qu'un choix. Elle se signale,
  elle ne se propage pas. Seule une exception écrite dans le régime d'autorisation la rend
  légitime -- et ce document appartient au propriétaire du dépôt, que l'agent n'écrit pas.

  **Quand cette contrainte sépare le code de la prose, la moitié « prose » ne tient que par
  prescription**, et c'est une faiblesse connue : un agent qui vient de lire des heures de code écrit
  sa prose dans le registre de la source, les tokens de celle-ci pesant sur la complétion autant que
  l'instruction. Aucun contrôle ne la couvre. La relecture humaine est le seul filet.
- **N5 -- Pas d'abstraction spéculative.** Aucune abstraction nouvelle sans une raison formulable en
  une phrase et au moins deux usages immédiats.
- **N6 -- Documentation du non-trivial.** Toute unité publique non triviale porte une documentation
  qui donne le contexte d'usage, les contraintes non évidentes et un exemple autonome.
- **N7 -- Une action non réversible clôt sa séquence.** Elle est le dernier acte de sa séquence et
  porte sur une donnée produite par cette séquence.
- **N8 -- Ce qui est consommé a son propre producteur.** Une action qui consomme un élément vérifié
  par un autre scénario a son propre scénario et son propre producteur.
- **N9 -- Observation, puis règle.** Ce qu'une conduite apprend est **consigné comme observation**
  dès que c'est constaté, dans le référentiel de sa nature. Une observation devient une **règle** à
  trois conditions cumulatives : réutilisabilité démontrée hors du cas qui l'a fait naître, absence
  de règle équivalente déjà présente, confirmation sur un second contexte. À défaut elle reste une
  observation, porte sa date, et se tranche à la consolidation suivante : promue ou **retirée**.

  Consigner ne dépend pas du succès de la conduite et coûte peu ; promouvoir engage le lecteur
  suivant. D'où l'asymétrie : la consignation est immédiate, la promotion est conditionnelle et
  datée. Sans l'échéance, la distinction entre observation et règle devient nominale -- tout reste,
  et l'attente ne coûte rien à personne.

  Un référentiel qui grossit sans critère finit illisible, et une règle qu'on ne lit pas ne contraint
  rien. En cas de doute, préférer enrichir une règle existante plutôt qu'en ajouter une.
- **N10 -- Un contrôle sans cible échoue.** Un contrôle dont la cible est absente du disque
  **échoue**, il ne passe pas. Un contrôle qui retourne « aucun manquement » parce qu'il n'a rien
  trouvé à examiner est un faux vert, et c'est le plus dangereux de tous : il se présente comme une
  preuve.

  Une cible écrite en dur dans un script est admise -- un contrôle propre à un projet connaît
  légitimement l'arborescence de ce projet. Ce qui ne l'est pas, c'est qu'elle disparaisse en
  silence : toute résolution de cible produit un échec explicite quand la cible manque, jamais une
  liste vide.
- **N11 -- Une lacune ne justifie une règle que si elle a produit un défaut survivant.** Un
  obstacle rencontré puis rattrapé -- par un arrêt, par une fiche, par une correction tracée --
  démontre que le dispositif fonctionne : il ne demande rien de plus.

  Ce critère **précède** les trois conditions de N9 et les filtre. Sans lui, chaque conduite verse ce
  qu'elle a trouvé pénible, et le protocole enfle de la mémoire de ses propres difficultés plutôt que
  de ses défaillances.

  **Trois questions à poser avant de proposer une règle, dans cet ordre :**

  1. le défaut a-t-il atteint le livrable, ou a-t-il été arrêté avant ? S'il a été arrêté, la règle
     est superflue ;
  2. une règle existante le couvrait-elle déjà, sans avoir été appliquée ? Si oui, le manquement est
     d'exécution, et écrire une règle de plus ne le corrigera pas ;
  3. la correction est-elle un **contrôle mécanique** ou une **prescription à lire** ? Un contrôle
     n'ajoute aucune charge au lecteur et se préfère toujours ; une prescription se paie à chaque
     lecture du protocole, par tous les agents suivants.

  Une lacune écartée par ce critère est **consignée comme écartée**, avec sa raison, dans le bilan de la conduite.
  Sans cette trace, la conduite suivante la re-proposera.

  **N11 filtre les règles nouvelles ; il ne filtre pas les contradictions.** Deux énoncés
  incompatibles du protocole se corrigent qu'un défaut ait atteint un livrable ou non : I7 interdit
  qu'ils coexistent, et la conduite suivante pourrait trancher autrement. Une contradiction se
  signale, se corrige, et n'a pas à démontrer qu'elle a coûté quelque chose.

### La doctrine propre au projet

Un projet peut porter des règles que le protocole n'a pas : elles vivent **dans la synthèse du
projet**, jamais dans un document créé pour elles. Le relevé d'amorçage dit où elles sont.

Une règle y entre si elle satisfait les quatre critères, et elle n'y entre pas autrement :

1. elle est **applicable sans jugement** -- une règle qui demande d'apprécier n'est pas une règle,
   c'est une intention ;
2. elle **répond à un arbitrage qui se répète**, et non à un cas unique ;
3. elle n'est **pas déjà portée** par la doctrine N1 à N11 ;
4. elle **cesserait d'avoir un sens** sur un projet d'une autre technologie -- sinon elle appartient
   au protocole général, et sa place s'y discute.

**Un projet n'a rien à déclarer de plus.** Les deux tables du contrat de correction sont fournies par
ce document ; un projet qui ne fournit aucun contrôle statique n'a pas à s'en justifier d'avance, le
relevé d'amorçage le constate.

---

# Partie II -- Le pipeline

## Amorçage : les trois préconditions de P0

**C'est l'agent qui réclame, pas l'humain qui doit y penser.** Une consigne rangée dans un document
que l'humain devrait se rappeler de lire n'est pas une garantie : elle est oubliée.

Trois préconditions doivent être remplies avant P0. **Deux appartiennent au propriétaire du dépôt ;
la troisième, l'agent l'exécute lui-même.**

| Précondition | Ce que l'agent fournit avec | Qui l'exécute |
|---|---|---|
| Le ticket existe | un titre et la description de ce qui est attendu | **L'agent, quand le propriétaire l'y a autorisé et qu'il dispose de l'accès.** À défaut, le propriétaire : le suivi de projet vit hors du dépôt et lui appartient |
| La session est pré-autorisée | la commande exacte, donnée par le régime d'autorisation | Le propriétaire : le mode se choisit au lancement du CLI, donc en relançant la session |
| La branche du sujet est la branche courante | — | **L'agent**, dès que le numéro de ticket est connu. C'est une opération d'ajout |

**Ce que la création du ticket par l'agent apporte, et ce qu'elle n'apporte pas.** Elle supprime un
aller-retour et fait démarrer la conduite sans attente. Elle n'est **pas** plus sûre en soi : un
agent qui demande le ticket peut parfaitement attendre le numéro réel avant de nommer la branche, et
il n'a jamais besoin de le deviner. Le gain est d'autonomie, pas de sûreté, et c'est à ce titre qu'il
se décide.

**L'accès n'est pas l'autorisation.** Disposer d'un jeton sur le suivi de projet ne signifie pas que
le propriétaire veut que l'agent y écrive. L'autorisation est explicite, elle est déclarée dans le régime
d'autorisation, et elle se retire en le modifiant.

Trois garde-fous quand l'agent crée le ticket :

- **chercher les tickets ouverts par sujet**, et non seulement lister les plus récents : un doublon
  peut porter sur un ticket ancien resté ouvert, que les dernières entrées ne montrent pas ;
- ne jamais fermer ni modifier un ticket existant ;
- en cas de doute sur l'existence d'un doublon, demander plutôt que créer.

**Le premier acte de l'agent est de vérifier ces trois préconditions, puis de ne demander que celles
qui manquent.** Le nombre de demandes n'est donc pas fixe :

| Situation | Ce que l'agent demande, puis attend |
|---|---|
| Sujet neuf, session non pré-autorisée, **accès et autorisation** de créer le ticket | la pré-autorisation seule -- il crée le ticket et la branche |
| Sujet neuf, session non pré-autorisée, sans autorisation **ou** sans accès | le ticket, et la pré-autorisation |
| Sujet neuf, session déjà pré-autorisée, **accès et autorisation** de créer le ticket | **rien** -- il crée le ticket, crée la branche et démarre |
| Sujet neuf, session déjà pré-autorisée, sans autorisation **ou** sans accès | le ticket seul |
| Reprise d'un travail en cours, session non pré-autorisée | la pré-autorisation seule |
| Reprise d'un travail en cours, session pré-autorisée | **rien** -- il vérifie que la branche du sujet est la branche courante et démarre |

**Demander une précondition déjà remplie n'ajoute aucune sûreté** : cela renvoie à l'humain une
décision que l'état du dépôt a déjà tranchée, et brouille le signal d'une demande véritable.

**En reprise, l'agent s'arrête** si la branche du sujet n'est pas la branche courante.

**Nom de branche.** La convention est celle du protocole, sauf exception déclarée par le régime
d'autorisation. Le numéro du ticket en fait généralement partie,
donc la branche se crée **après obtention du numéro** -- que l'agent ait créé le ticket lui-même ou
qu'il l'ait demandé. L'agent annonce le nom retenu en
créant la branche et ne le soumet pas à validation : la convention est fermée, et un nom qui la
respecte n'appelle pas d'arbitrage.

**Pré-autoriser les outils du CLI.** L'agent enchaîne compilations, contrôles statiques, exécutions
et écritures d'artefacts. Un prompt d'autorisation par commande le bloque à chaque maillon, et lui
fait ré-approuver commande par commande ce que le manifeste a déjà déclaré.

Ce que cette pré-autorisation retire, et qu'il faut savoir avant de la donner : le prompt du CLI est
le seul contrôle **préventif** que ce document décrive. S'il en existe d'autres -- droits du système,
bac à sable, restrictions de l'environnement -- ce protocole n'en suppose aucun. La pré-autorisation
complète laisse les risques résiduels au propriétaire du dépôt, qui les accepte en les déclarant dans son
régime d'autorisation.

**Les mutations prévues par le périmètre n'exigent pas d'approbation individuelle.** Ce que le
travail consiste à faire, il le fait. Les actions irréversibles restent régies par N7 et N8 : la
pré-autorisation porte sur le prompt de l'outil, pas sur la conception des scénarios.

## Connaissances préalables, obligatoires avant P0

La synthèse du projet, et les documents qu'elle désigne comme normatifs, doivent être lus avant
d'ouvrir le pipeline, et rester disponibles jusqu'à l'analyse. Leur contenu ne se redécouvre pas
depuis le seul code : une partie y est certes observable, mais au prix d'une exploration que ces documents évitent, et le reste ne s'en déduit
pas -- vocabulaire métier, décisions de conception, conventions, et pièges qui ont déjà coûté cher.

Chaque entrée porte sa nature : **connaissance** que l'on consulte, ou **normatif** auquel on se
conforme.

**Il n'y a jamais zéro connaissance préalable.** Un projet qui n'aurait rien à faire lire commence
par écrire ce document.

**L'obligation ne dépend d'aucune phase.** Elle vaut pour une conduite partielle comme pour une
conduite complète, quelles que soient les phases exécutées. Trop lire coûte du contexte, ne pas lire
coûte un défaut que seule une exécution révèle, et parfois rien ne révèle.

Un document normatif dont l'objet est absent de la conduite se lit quand même, et la conduite écrit
qu'il est sans objet -- c'est une décision tracée, pas un silence.

### Les référentiels de conception, imposés par le protocole

**Trois documents sont normatifs pour toute conduite, quel que soit le projet.** Ils ne sont pas
désignés par le projet : le protocole les impose, et un projet n'a rien à déclarer pour qu'ils
s'appliquent.

| Document | Ce qu'il apporte |
|---|---|
| `../../regles/conception.md` | Règles de conception : conception orientée résultat, KISS, DRY, **YAGNI**, responsabilité unique, cohésion forte et couplage faible, OCP, séparation modèle métier et orchestration, évitement du null, immuabilité |
| `../../regles/codage.md` | Conventions de codage et de nommage : principes directeurs, commentaires, conventions git, nommage des modules, types, fonctions, variables, documentation |
| `../../llm/conception_de_code_pour_llm.md` | Conception LLM-friendly : réduction de la variance, noms auto-décrivants, classes courtes et cohésives, patterns consistants, documentation à exemples complets, messages d'erreur explicites, paramètres explicites plutôt qu'état implicite, abstractions non spéculatives, constantes nommées |

Les références relatives de cette section se résolvent depuis le dossier de ce fichier de
protocole, jamais depuis le répertoire courant. Avant de les lire, les convertir en chemins absolus
et vérifier leur existence ; une référence introuvable est un arrêt.

**Ils se lisent avant P0, et pas à P4.** C'est le point qui coûte le plus cher quand on l'oublie,
parce que leurs règles infléchissent le **cadrage** et non seulement la conception détaillée. YAGNI en
particulier ne se rattrape pas après coup : un cadrage qui a déclaré des artefacts « pour plus tard »
les voit repris en aval sans être questionnés, et chaque phase suivante les tient pour acquis. Lire
tard un référentiel normatif, c'est ne pas l'appliquer.

Ils complètent la doctrine N1 à N11 sans la remplacer. En cas de contradiction entre l'un d'eux et
une règle N, la règle N l'emporte, et l'écart se signale dans le bilan de la conduite.

### Ce que le projet ajoute

**Le relevé d'amorçage est l'unique autorité sur les documents du projet.** Il énumère ceux-ci,
leur nature et leur chemin ; il ne redéclare **jamais** les trois référentiels ci-dessus, et RA5 du
gabarit d'analyse ne répète ni l'une ni l'autre liste.

**Les deux autorités ne se recouvrent pas** : le protocole possède la liste universelle, le relevé
possède celle du projet. Deux déclarations d'une même liste divergent à la première évolution, et la
divergence est silencieuse -- un agent qui lit l'une croit légitimement avoir tout lu.

Ne pas confondre consultation et cartographie. Ces documents décrivent l'architecture ; ils ne
dispensent pas d'aller lire le code réel, et un fait recopié dans une analyse se source toujours sur
le fichier, jamais sur la synthèse. Les synthèses peuvent avoir vieilli : **une contradiction entre
une synthèse et le code se tranche en faveur du code**, et se signale.

## Les huit phases

Chacune produit un artefact vérifiable et déclare ce que l'agent a le droit d'écrire. Une phase ne
commence pas tant que l'artefact de la précédente n'existe pas.

| Phase | Nom | Artefact produit | Surface d'écriture autorisée |
|---|---|---|---|
| P0 | Cadre et référence | `baseline_<theme>.md`, autonome ; **plus, pour une correction d'anomalie, la preuve rouge** | Ce fichier seul ; **plus, pour une correction d'anomalie, la preuve rouge et son dispositif d'exécution, déclarés dans la baseline avant d'être écrits** |
| P1 | Cartographie de l'existant | Rapports de faits sourcés | Le dossier de cartographie du chantier |
| P2 | Cadrage | `cadrage_<theme>.md` | Le cadrage seul |
| P3 | Preuve observée | Fichiers de faits | Instrumentation probatoire déclarée, son dispositif d'exécution et le dossier de faits |
| P4 | Analyse détaillée | `analyse_detaillee_<theme>.md` | L'analyse seule |
| P5 | Plan d'implémentation | `plan_implementation_<theme>.md` | Le plan seul |
| P6 | Implémentation et validation | Code, données, exécution verte ou diagnostic | Les seuls fichiers énumérés par le plan |
| P7 | Clôture | Référentiels et matrices à jour, bilan | Référentiels, matrices d'avancement et documents de clôture |

### P0 - Cadre et référence

Établir l'état de départ avant toute modification, faute de quoi aucun écart constaté plus tard ne
sera imputable. Relever la branche et le commit courants, l'environnement cible, les modifications
locales à préserver, et les phases que la conduite exécutera.

Si la tâche est donnée par un ticket, le lire avant de cadrer le travail et consigner dans la
baseline son URL ainsi que sa date de consultation ; s'il est inaccessible, s'arrêter.

**Le travail vit sur une branche dédiée au sujet.** P0 ne commence pas tant que cette branche n'est
pas la branche courante. Si la branche courante est la branche principale, s'arrêter et le signaler.

Exécuter la validation de non-régression la plus proche du périmètre, et consigner son résultat avec
le chemin absolu de son artefact. Une baseline rouge n'interdit pas de continuer, mais elle change le
statut de tout échec ultérieur.

**Amorçage sans validation initiale.** Si le projet ne possède encore aucune validation exécutable,
consigner `ABSENT` au départ et prévoir la création du premier contrôle dans la surface autorisée.
Son attendu est fixé avant l'implémentation du comportement contrôlé. À la clôture, exécuter la
validation ainsi créée : l'absence de validation initiale ne dispense pas de validation finale.
Si aucun contrôle pertinent ne peut être défini, rendre la main.

**Pour un correctif, la baseline porte la preuve rouge avant P1.** Elle en précise l'origine,
le rattachement au défaut, le comportement constaté et l'oracle prévu pour vérifier l'état corrigé.
Une preuve existante respecte les conditions des « Observations héritées ». P4 en confirme ou
invalide la suffisance ; il ne remplace pas son établissement en P0. Une preuve inaccessible
ou insuffisante relève d'E9, avec la portée d'arrêt définie par le protocole.

La table des surfaces borne les écritures nécessaires à cette preuve. **Aucune correction du défaut
ni modification du code suspecté en P0.** Tout fichier est déclaré dans la baseline avant écriture ;
un besoin hors de cette surface relève d'E6.

La baseline distingue la sonde temporaire, soumise à S1–S8, du test destiné à rester dans le projet.
Ce test est déclaré dans le périmètre du plan en P5 pour son utilisation ou sa modification en P6.

#### Le relevé d'amorçage

**P0 consigne ce que l'agent a trouvé en regardant.** C'est ce qui remplace une annexe pré-remplie :
un fait relevé et daté vaut mieux qu'un fait pré-écrit qui vieillit sans que rien ne le signale.

Chaque ligne se source -- chemin absolu, et ligne quand elle existe. Une ligne dont la réponse est
introuvable s'écrit `ABSENT`, jamais par une valeur plausible.

| Ce que le relevé établit | Où l'agent le trouve, typiquement |
|---|---|
| La commande de lancement, et les lanceurs à ne pas employer | La synthèse du projet, son guide de contribution, ses scripts |
| Ce qui prouve qu'une exécution a eu lieu, et où se lit son verdict | Le même, plus un artefact d'exécution réel |
| **Si le verdict est binaire ou non**, et ce qui tient lieu de critère quand il ne l'est pas | Le dispositif de validation lui-même |
| Comment prouver qu'on examine l'artefact de la bonne exécution | Idem |
| Les canaux de preuve disponibles par couche suspecte, **et ceux qui manquent** | La suite de tests et l'outillage de mesure |
| **Les documents à lire avant P0**, chacun avec sa nature -- connaissance ou normatif | La synthèse du projet, et ce qu'elle désigne. **Cette ligne fait autorité** : aucun autre document ne redéclare la liste |
| Les référentiels où ce que la conduite apprendra sera versé | La synthèse, le backlog, le référentiel de pratiques |
| Les artefacts qu'une exécution modifie et qui n'appartiennent à aucun périmètre | Le fichier d'exclusions de version, croisé avec ce qu'une exécution touche |
| Le contrôle statique du projet s'il existe, **et ce qu'il ne couvre pas** | Le script, ou son absence |
| La **convention applicable** et la **conformité observée** | Le référentiel imposé, le régime d'autorisation, puis le code -- dans cet ordre |
| La correspondance entre les artefacts du projet et les tables du contrat de correction | Ce que la cartographie du dépôt établit |

**Deux lignes portent une négation, et ce n'est pas un détail de rédaction.** Un canal de preuve qui
manque rend une couche inobservable -- c'est un **E9** à venir, pas une invitation à improviser. Un
contrôle statique dont on ignore les angles morts est lu comme une preuve plus forte qu'il n'est.
Aucune synthèse d'architecture n'écrit ce qu'elle ne couvre pas ; le relevé, si.

**Ce qui s'avère durable remonte dans la synthèse du projet en P7**, par N9. Le relevé n'a pas
vocation à être refait à l'identique à chaque conduite : la synthèse grossit par l'usage, et le
relevé suivant se réduit à vérifier ce qu'elle porte déjà. C'est la parade à la décision rejouée.

Ces faits vont dans un fichier **autonome**, `baseline_<theme>.md`, et non dans le cadrage : celui-ci
n'existe qu'en P2, et une phase ne peut pas produire un artefact qu'elle n'a pas le droit d'écrire.
Le cadrage reprendra ces faits par référence.

### P1 - Cartographie de l'existant

Rassembler les faits nécessaires au cadrage sans les redécouvrir plus tard. L'exploration large est
déléguée à des sous-agents, en parallèle, avec une consigne fermée : recopier, sourcer par chemin
absolu, écrire `ABSENT` quand l'information n'existe pas, ne rien recommander.

Le travail des sous-agents est vérifié avant usage. Deux modèles de la même famille partagent les
mêmes angles morts : un rapport de sous-agent est une source, pas une preuve. La vérification porte
en priorité sur ce qui sera recopié, c'est-à-dire les signatures, les chemins et les valeurs exactes.

**C'est ici que les documents de conception préexistants sont consommés** -- voir « Un projet déjà
entamé » plus bas.

### P2 - Cadrage

Le cadrage fixe ce qui est décidé et énumère ce qui reste à observer. Il ne contient aucune valeur
non observée. Son critère de complétude : l'analyse détaillée doit pouvoir être écrite sans rouvrir
une décision de conception.

Format imposé : `gabarit_cadrage.md`.

### P3 - Preuve observée

Pour un correctif, P3 établit la cause à partir de la preuve du défaut, sans figer de valeurs neuves.
Si le défaut ne se reproduit pas alors qu'il le devrait, investiguer séparément cette contradiction
et la mesurer avant toute correction. La méthode de diagnostic propre au projet, si elle existe,
est désignée par sa synthèse et s'applique dans P1, P3 et P4, sous les mêmes règles de bornage et d'arrêt.

Toute inconnue listée par le cadrage est levée par une observation réelle, produite par une
instrumentation probatoire exécutée comme une exécution normale.

**Le canal de preuve dépend de la couche suspecte**, et il se choisit dans le relevé d'amorçage de P0. Le principe ne bouge
pas -- aucune valeur non observée -- mais toute observation n'a pas le même canal, et réclamer un
canal inadapté créerait une phase artificielle. Une couche suspecte pour laquelle le relevé ne trouve aucun
canal est un **E9**, pas une invitation à improviser un canal.

**Observer coûte, et ce coût se choisit.** Une observation qui n'exige pas de donnée fraîche se fait
sur la variante la plus courte qui pointe une donnée déjà produite, et non sur une séquence complète
qui rejoue son producteur à chaque passe. Seules les observations qui consomment ou modifient la
donnée imposent la séquence complète.

Le gain croît avec la longueur de la séquence. Sur deux maillons il reste marginal ; sur une séquence
qui enchaîne plusieurs producteurs avant le maillon travaillé, il approche l'exécution entière. La
marche à suivre : un premier passage en complet, puis épingler dans un jeu de données court les
valeurs que le producteur a produites, et itérer dessus.

**On itère sur le court, on valide sur le complet.** Un vert sur variante courte ne vaut pas
livraison : il atteste un comportement sur une donnée préparée, pas la séquence que le périmètre
déclare. Cette règle vaut aussi dans la boucle de correction, où le plafond de deux tentatives rend
le temps de cycle déterminant.

Si une observation s'avère impossible, la ligne concernée est déclarée bloquée et le travail continue
sur son périmètre restant. Elle n'est jamais complétée par une valeur plausible.

### P4 - Analyse détaillée

Pour un correctif, nommer la cause racine, la couche responsable et la contre-indication :
le fait qui invaliderait le diagnostic.

L'analyse résout les inconnues du cadrage à partir des observations, fige les valeurs et descend au
niveau fichier. Chaque valeur figée cite l'observation dont elle provient.

**Tout fait décisionnel reçoit un statut explicite.** Un fait d'observation est décisionnel dès qu'il
pourrait infléchir une valeur, un oracle ou une structure de scénario. Chaque fait décisionnel entre
dans la table des faits observés de l'analyse et y porte l'un de trois statuts : utilisé par la
conception, contrainte prise en compte, ou écarté avec sa raison. **L'analyse n'est pas close tant
qu'un fait décisionnel reste sans statut.**

L'exigence est bornée aux faits décisionnels : l'étendre à chaque ligne d'observation brute
produirait du remplissage mécanique, sans valeur.

Elle traite un défaut que le sourçage n'attrape pas. Le protocole exige de tout sourcer et de ne rien
inventer ; il n'exige nulle part de **relire ses propres faits contre sa conception**. Une décision
peut être prise, complète, et fausse au regard d'un fait déjà relevé.

Format imposé : `gabarit_analyse_detaillee.md`.

### P5 - Plan d'implémentation

Le plan est exécutable par un agent froid et faible : aucune décision de conception restante, aucun
choix à faire, aucune référence à une variable définie ailleurs. Il énumère les fichiers à créer ou
modifier avec leur chemin absolu et leur contenu.

Le plan **ne contient aucune commande git comme étape de travail** : les points de commit sont une
obligation permanente, énumérée dans « Ce que l'agent fait avec git », et non une décision de
conception à rejouer dans chaque plan.

Format imposé : `gabarit_plan_implementation.md`.

### P6 - Implémentation et validation

Pour un correctif, l'oracle appliqué à l'état corrigé vérifie la disparition du comportement
attesté par la preuve rouge et le comportement attendu, puis la non-régression pertinente.

L'agent applique le plan, puis dans l'ordre : contrôle statique par script, contrôle de compilation
ou équivalent, puis exécution. Un échec ouvre la boucle de correction encadrée.

La surface d'écriture est exactement l'ensemble des fichiers énumérés par le plan. Tout autre fichier
est en lecture seule pour toute la phase.

### P7 - Clôture

Mettre à jour les référentiels et les matrices d'avancement, **faire entrer les validations vertes
dans la campagne de non-régression**, écrire le bilan et **vérifier** que les
artefacts temporaires ont disparu.

#### Une validation verte entre dans la campagne

**Toute ligne dont le statut devient « fait » voit sa validation entrer dans la campagne de
non-régression relevée en P0, ou la raison de son exclusion est écrite dans la campagne elle-même.**

Une validation verte absente de toute campagne ne protège de rien : rien ne la rejoue, et son verdict
ne vaut que pour le jour où il a eu lieu. C'est le seul moment où l'ajout est gratuit -- plus tard,
personne ne saura si elle est encore verte.

**Validée où ?** Sur l'environnement de la campagne. Une validation obtenue sur un autre environnement
est rejouée sur celui-ci avant d'y entrer ; sinon, c'est la campagne qu'on casse.

**Une exclusion s'écrit dans la campagne, avec l'obstacle qui la motive** -- en commentaire, à sa
place, et non par omission. Une ligne simplement absente est indiscernable d'un oubli.

Les lacunes du protocole rencontrées et les corrections proposées se consignent dans le bilan de
la conduite. Les pratiques propres au projet vont dans le référentiel relevé en P0.

**L'agent ne modifie ni le protocole, ni le régime d'autorisation.** Verser une règle
dans un document normatif appartient au propriétaire, sur proposition écrite. Un agent qui corrige le
protocole au passage se donne raison sans arbitre.

Une conduite qui ne remonte rien l'écrit aussi : c'est un constat, pas un silence.

**Le retrait des artefacts temporaires n'appartient jamais à P7.** Il appartient à P6 quand un plan
existe : l'instrumentation probatoire y est déclarée, donc supprimée par une étape du plan. Quand la
conduite s'arrête avant P5 et qu'aucun plan n'existe, le retrait est le **dernier acte de la phase
qui a créé l'artefact**, c'est-à-dire P3. Dans les deux cas la phase qui supprime est celle qui a
déclaré l'artefact dans sa surface d'écriture. P7 ne fait que constater l'absence.

Le retrait reste soumis à S8 : l'artefact est commité avant d'être supprimé.

## Les artefacts opérationnels globaux

Les artefacts opérationnels globaux relevés en P0 sont modifiables dans **toutes** les phases, sans sauvegarde ni
restauration. Ils n'appartiennent à aucun périmètre applicatif et n'entrent dans aucun manifeste de
contrôle. Aucune ligne de plan ne leur est consacrée.

**La porte de publication les ignore, et les commiter est facultatif.** Ils sont modifiés par
presque chaque exécution : exiger qu'ils soient commités mettrait un point de commit sans contenu à
chaque lancement, et exiger qu'ils soient propres bloquerait la publication en permanence. Leur état
ne dit rien de la cohérence du travail livré, ce qui est précisément ce que la porte évalue.

Ils ne sont pas pour autant sans conséquence, et c'est la nuance qui compte : leur état détermine ce
que la prochaine exécution fait. Une sélection erronée ne dégrade pas le produit livré, mais elle
peut faire valider un périmètre qui n'est pas celui qu'on croit.

D'où la contrepartie, qui est une exigence de traçabilité et non de préservation : **toute validation
par exécution doit prouver qu'elle examine l'artefact de la séquence attendue**, et non simplement le
plus récent. Le moyen de cette preuve est relevé en P0.

## La conduite partielle, déclarée

Toutes les phases ne sont pas toujours pertinentes. Une mesure, une observation, une investigation ne
livrent aucun code : P5 et P6 sont sans objet.

**Les phases exécutées sont annoncées au démarrage et écrites dans la baseline de P0.** Ce qui ne
change jamais : le régime d'autorisation et la synthèse du projet sont lus, le contrat de
correction est porté par un document, et P7 a lieu.

**Une conduite partielle déclarée doit rester moins coûteuse qu'un contournement silencieux**, sinon
personne ne la déclare. C'est une règle de conception du protocole autant qu'une règle d'usage :

- déclarer une phase sans objet coûte **une ligne** dans la baseline, avec sa raison ;
- sauter une phase sans le dire ne coûte rien sur le moment, et coûte l'intégralité des garanties
  ensuite, sans que rien ne le signale.

Un agent qui hésite entre les deux prend la première. Un agent à qui le protocole rendrait la
déclaration pénible prendrait la seconde -- et c'est le protocole qui aurait tort.

**Ce qui n'est jamais une conduite partielle légitime :** sauter P3 parce que l'observation coûte,
sauter P4 parce que la conception paraît évidente, ou sauter le contrat de correction parce qu'aucun
échec n'est attendu. Ces trois-là sont des contournements, et ils se reconnaissent à ce qu'ils
n'énoncent aucune raison vérifiable.

## Un projet déjà entamé

C'est le cas courant, pas l'exception. Il ne demande aucun régime particulier, à condition de tenir
deux distinctions.

### Le protocole porte un incrément, pas une base de code

On ne réapplique jamais le protocole à un existant : on l'applique au **prochain incrément**, et tout
ce qui précède est de l'existant que P1 cartographie. Le coût est proportionnel à l'incrément, pas à
l'historique.

Il n'y a donc pas de « protocole à rattraper » sur un projet en cours. Il y a une évolution à
conduire, dont l'existant est une entrée comme une autre.

### Un artefact de conception préexistant est une source, jamais une entrée normative

Un plan, une spécification, un document de conception rédigés hors de ce protocole **n'ont aucune
autorité**. Ils sont cartographiés en P1 comme n'importe quel document existant, soumis aux règles
ordinaires : recopier, sourcer par chemin absolu, écrire `ABSENT`, ne rien recommander.

Ce sont des **synthèses**. La règle des connaissances préalables s'applique intégralement : un fait
se source sur le fichier, jamais sur la synthèse, et une contradiction entre une synthèse et le code
se tranche en faveur du code.

**Pourquoi ne pas les admettre comme entrées et sauter les phases amont.** Ce serait la voie
apparemment économique, et c'est un faux vert au niveau du processus. Un plan produit hors protocole
ne porte ni surface d'écriture déclarée, ni contrat de correction, ni critères de validation définis
avant exécution. Décider s'il les porte demanderait de l'auditer, c'est-à-dire de certifier un
document dont on ne connaît pas les conditions de production -- au moins aussi cher que refaire
l'analyse, et beaucoup moins fiable. Un plan étranger bien rédigé passerait un tel audit sans porter
aucune des garanties qu'il semble porter.

**Conséquence assumée : le plan préexistant sera réécrit.** Ce n'est pas du travail perdu -- il sert
de source et raccourcit la cartographie et l'analyse -- mais le livrable de P5 est un plan produit
sous ce protocole, pas le document d'origine annoté.

### Quand le prompt de démarrage contredit le protocole

Un prompt dit souvent d'un document préexistant qu'il est la « source de vérité ». La formulation est
naturelle, et elle entre en conflit avec la règle ci-dessus. Le partage est fermé :

| Ce que le prompt fixe | Ce que le protocole fixe |
|---|---|
| L'objet de la tâche, son périmètre, ce qu'il ne faut pas élargir | La méthode : ce qui se vérifie, ce qui se source, ce qui a autorité |

Un prompt qui appelle un document « source de vérité » **délimite le travail** : ne pas s'écarter de
ce qu'il décrit, ne pas traiter un autre sujet. Il ne suspend pas l'obligation d'en vérifier les
faits. Lue comme une dispense de vérification, la formule ferait entrer dans la conduite des faits
dont personne n'a établi qu'ils sont encore vrais -- et le défaut serait invisible, puisque la
vérification est précisément ce qui aurait été sauté.

**Si le propriétaire veut réellement dispenser de la vérification, cela ne passe pas par un prompt.**
C'est une décision : elle vit dans le régime d'autorisation, elle porte sa date et sa raison. Un
prompt s'écrit vite et ne se relit pas ; une décision datée, si.

En cas de doute, l'agent applique la règle du protocole et **écrit dans sa baseline** qu'il l'a fait,
avec la phrase du prompt qui l'a fait hésiter. Il n'interrompt pas pour cela : la portée du prompt
est le périmètre, celle du protocole est la méthode, et les deux ne se recouvrent pas.

### Les observations héritées, seul vrai cas d'héritage

Un document se réécrit ; une observation ne se re-dérive pas. Si un chantier antérieur a produit des
relevés dans des conditions qui n'existent plus -- environnement disparu, donnée consommée, version
changée -- P3 ne les reproduira pas.

Une observation héritée n'est utilisable comme **preuve** qu'à trois conditions cumulatives :

1. ses conditions de production sont documentées et vérifiables dans la preuve brute, et non
   seulement dans une synthèse qui la résume ;
2. elle est passée par le **même dispositif** que toute observation neuve à laquelle on la compare --
   même canal, même critère de stabilisation, même granularité. C'est S7 appliqué entre deux
   conduites au lieu d'une ;
3. rien n'a changé entre-temps dans ce qu'elle mesure, et ce constat est écrit.

Si l'une manque, l'observation héritée reste une **source d'orientation** -- elle dit où regarder --
et n'est jamais un oracle. La conduite ré-observe, ou déclare l'observation impossible et escalade en
**E9**. Elle ne complète jamais l'écart par une valeur plausible.

**Un décompte d'observations héritées se recompte sur les preuves brutes.** Une synthèse peut avoir
perdu les conditions des observations qu'elle compte, et le défaut est en aval de tout contrôle :
il ne se produit ni dans une capture ni dans une analyse, mais dans le document qui les résume.


---

# Partie III -- Documents et contrôles

## Documents à format imposé

| Document | Rôle | Lecteur cible |
|---|---|---|
| Régime d'autorisation | Porte les décisions du propriétaire du dépôt | Tout agent, avant P0 |
| Relevé d'amorçage | Consigne ce que l'agent a trouvé en regardant | L'agent lui-même, en P0 |
| Cadrage | Fixe les décisions, énumère les inconnues | L'agent qui écrit l'analyse détaillée |
| Analyse détaillée | Résout les inconnues, descend au niveau fichier | L'agent qui écrit le plan, ou qui conclut quand la conduite n'en produit pas |
| Plan d'implémentation | Séquence d'actions sans décision restante | Un agent froid et faible qui exécute |
| Fiche de faits observés | Observation sourcée, une entrée par élément observé | L'agent qui fige les valeurs |
| Notes d'exécution | Une fiche par échec, écrite avant toute correction. Section du document qui porte le contrat de correction | Le superviseur en audit, et l'agent après un effacement de contexte |

Trois exigences communes :

- **chemins absolus systématiques** ;
- **zéro contradiction interne, et zéro contradiction avec un document amont** ;
- **zéro bruit historique** : ce qui est déjà dans le code ou dans git n'a rien à faire dans un
  document de contexte.

## Documents à format libre

Le bilan, les rapports de cartographie et les notes de travail. Ils ne sont pas consommés comme
entrée normative par une phase suivante. Un rapport de cartographie reste soumis à l'exigence de
sourçage.

## Ce qui fait un bon document

- **Écrire pour un lecteur qui n'a pas la conversation.** Ce qui a été décidé oralement doit figurer
  dans le document, sinon la décision n'existe pas.
- **Une règle par ligne, vérifiable.** Une phrase qui contient deux règles est appliquée à moitié.
- **Dire ce qui est interdit, pas seulement ce qui est attendu.**
- **Ne jamais poser de quota.** « Lister toutes les inconnues » et non « les trois principales » : un
  quota est satisfait par remplissage.
- **Nommer les valeurs, pas les décrire.**
- **Marquer l'inconnu comme inconnu.** Un fait non observé s'écrit `ABSENT` ou « à observer », jamais
  sous forme d'une valeur plausible assortie d'un conditionnel.

## Écrire pour un lecteur qui utilise grep

Ces documents ne sont pas lus en entier : un agent les ouvre par recherche puis lit une fenêtre autour
du résultat. Le format décide donc de ce qu'il trouve, indépendamment du contenu.

- **Une entité, un bloc.** Un fait observé, une décision, une fiche de KO tiennent d'un seul tenant.
  Lire N lignes depuis son titre doit donner l'entité complète, sans reconstruction.
- **L'identifiant dans le titre du bloc.** Le chemin de fichier, le numéro de décision ou le nom du
  champ vit dans le `###`, pas seulement dans le corps.
- **Pas de valeur multiple dans une cellule.** Une ligne par valeur, ou une liste à puces.
- **Pas de champ que la procédure n'utilise pas.** Une colonne systématiquement vide, un libellé
  dérivé mécaniquement d'un identifiant voisin, une colonne en doublon : ce sont des tokens sans
  signal, et ils diluent le reste.
- **Nommer à la granularité réelle.** Un champ nommé pour une granularité plus fine que la donnée
  qu'il porte produit une fausse précision. Quand la granularité est plus grossière que le format ne
  le suggère, le dire **dans les données**, pas seulement dans la documentation.
- **Vocabulaire neutre pour les métadonnées d'exécution.** Un champ nommé `retry`, `fallback` ou
  `echec` oriente le diagnostic vers l'instabilité même quand il décrit un paramétrage sans rapport
  avec la cause. Nommer ce qui est décrit, pas ce qu'on en craint.

## Contrôle déterministe

Le contrôle statique est la seule validation admise en dehors de l'exécution. Il retourne un code de
sortie et n'émet aucun jugement. Il remplace l'auto-relecture de l'agent, qui n'a aucune valeur de
validation.

### Le manifeste de conduite

Un fichier par conduite, qui déclare le document portant le contrat de correction et le périmètre --
fichiers créés **et** modifiés. Le périmètre déclaré **est** la surface d'écriture autorisée : un
fichier absent du manifeste n'a pas à être modifié par la conduite.

**Les listes de périmètre peuvent être vides**, quand la conduite ne livre rien. Une liste vide est
une déclaration, à condition que le manifeste dise pourquoi.

**Tout chemin déclaré est relatif à la racine, sans remontée, et ne désigne pas la racine.** Un chemin
absolu ou remontant reste lisible par les contrôles de contenu -- une bibliothèque de chemins le résout
sans broncher -- mais git ne produit que des chemins relatifs au sommet du dépôt. Le périmètre ne
correspondrait alors à rien de ce que git annonce, et un fichier déclaré mais non commité passerait
inaperçu à la porte de publication : un faux vert sur le contrôle même qui autorise à publier. Un
chemin désignant la racine est refusé pour une autre raison : il est relatif et sans remontée, mais il
place tout le dépôt dans le périmètre, ce qui vide le contrôle de son sens.

**Un manifeste qui y déroge est invalide, code `2`, et non porteur d'un manquement.** L'erreur rend
les contrôles ininterprétables plutôt qu'elle ne révèle un défaut du code livré. Le contrôle est fourni
par `verifier_chemins_declares.py`, indépendant du projet.

Ses autres clés nomment des artefacts propres au projet, et le relevé d'amorçage les décrit. Trois
clés sont imposées par le protocole :

| Clé | Ce qu'elle déclare | Quand elle est obligatoire |
|---|---|---|
| racine du dépôt | La racine réelle du dépôt de travail | Toujours |
| `contrat_de_correction` | Le document portant la conduite à tenir après un échec | Toujours |
| `branche_du_sujet` | La branche de **ce** ticket | Pour franchir la porte de publication |

`branche_du_sujet` n'est pas redondante avec la convention de nommage : la convention prouve la
*forme* d'une branche de sujet, elle ne prouve jamais qu'il s'agit de la branche de ce ticket-là.

### Codes de sortie, communs à tous les contrôles

| Code | Signification |
|---|---|
| 0 | aucun manquement |
| 1 | au moins un manquement détecté |
| 2 | manifeste absent, illisible ou incomplet |
| 3 | cible déclarée introuvable sur le disque -- voir N10 |
| 4 | porte de publication indécidable : git n'a pas répondu |

Le code `4` est distinct du `1` à dessein. Un manquement dit « la branche ne doit pas être poussée » ;
une porte indécidable dit « on ne sait pas », et les deux n'appellent pas la même conduite.

### Les contrôles indépendants du projet

Trois, à la racine du paquet. Aucun ne connaît la technologie de son dépôt.

| Contrôle | Quand | Ce qu'il garantit |
|---|---|---|
| `verifier_chemins_declares.py` | Avant tout autre contrôle | Le manifeste est interprétable |
| `verifier_contrat_de_correction.py` | Avant toute action, et de nouveau en P6 | L'exécutant sait quoi faire après un échec |
| `verifier_porte_de_publication.py` | En fin de conduite | L'état local est cohérent avec ce qui a été validé |

Un projet les appelle depuis son propre contrôle statique, pour que la conduite n'ait qu'une commande
à retenir. Chacun offre aussi un mode ligne de commande, pour un projet qui ne fournit aucun contrôle
statique.

### Le contrôle du contrat de correction, obligatoire et indépendant du projet

```text
python verifier_contrat_de_correction.py <chemin_du_document>
```

Il vérifie que le document qui porte le contrat de correction porte bien la conduite à tenir après un
échec, recopiée depuis ce protocole.

C'est le seul contrôle qui protège l'**exécutant** plutôt que le code livré. Une prescription de
recopie ne se vérifie pas par la lecture ; ce contrôle la transforme en barrière. Il échoue sur un
marqueur absent, jamais sur un contenu supplémentaire : il garantit une présence, il ne contraint pas
la rédaction.

**Il demeure obligatoire quelles que soient les listes du manifeste.** Une conduite partielle en a le
même besoin qu'une conduite complète, puisqu'elle agit et peut échouer.

**La clé `contrat_de_correction` nomme un rôle, pas un artefact** -- le plan quand la conduite en
produit un, le cadrage sinon.

### La porte de publication

Elle est décrite dans « Ce que l'agent fait avec git ». Sa logique est indépendante du projet ; ce
qu'elle doit savoir du dépôt ne l'est pas : les branches principales et la
convention de nommage par le régime d'autorisation, les artefacts opérationnels globaux par le
relevé d'amorçage, le périmètre par le
manifeste.

Elle s'invoque de deux façons, et une seule logique les sert :

- **depuis le contrôle statique du projet**, cas normal. Le périmètre d'un projet est réparti sur des
  clés qui lui sont propres ; seul son script sait les aplatir. Il appelle la porte en bibliothèque ;
- **en ligne de commande**, pour un projet qui ne fournit aucun contrôle statique et dont le
  manifeste déclare un périmètre à plat.

Le relevé d'amorçage dit laquelle des deux s'applique, et donne la commande.

### Les contrôles propres au projet

Ils portent sur le code livré et dépendent de la technologie. Le relevé d'amorçage les décrit : leur commande, ce
qu'ils contrôlent, et **ce qu'ils ne contrôlent pas**. Cette dernière colonne n'est pas optionnelle :
un contrôle dont on ignore les angles morts est lu comme une preuve plus forte qu'il n'est.

### Deux obligations de maintenance

- **Relancer tous les contrôles après tout déplacement de dossier.** Les chemins d'un manifeste
  archivé pointent une évolution passée : un rangement les casse silencieusement, et le seul artefact
  qui prouve que le contrôle fonctionne cesse alors de fonctionner sans que rien ne le signale.
- **Relancer tous les manifestes du dépôt, pas le seul manifeste courant.** Rien ne les relance
  mécaniquement.

## Lancer et lire un verdict

La commande de lancement est celle du relevé d'amorçage. C'est le seul moyen admis ; les lanceurs
que le relevé déclare interdits ne s'emploient jamais, et il dit pourquoi.

**Ne jamais conclure d'un code retour 0 que l'exécution a eu lieu.** La preuve d'une exécution est
l'artefact décrit par le relevé d'amorçage, et c'est lui qui porte le verdict.

**Ne jamais conclure d'une exécution verte qu'un comportement est stable tant qu'il n'a tourné qu'une
fois.** Une validation qui repasse au vert sans modification n'est pas réparée : elle porte une
contradiction non mesurée, et se traite comme telle.

Quand le verdict est KO, le premier artefact à lire est celui que le relevé d'amorçage désigne.
