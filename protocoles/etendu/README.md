# Protocole étendu

## Ce que ce paquet est

Un protocole de conduite d'une évolution, indépendant de la technologie du projet. Il formalise
l'état initial, organise les preuves dans des documents distincts et contrôle mécaniquement les
conditions de publication de la branche. Son application reste soumise au régime d'autorisation
du projet.

**Quasi-autonomie** veut dire une chose précise : l'agent décide et agit seul dans un périmètre
déclaré, et il s'arrête sur une liste fermée de cas. Ce n'est ni de l'autonomie -- il ne choisit ni
son périmètre ni le moment de publier -- ni de l'assistance -- il n'attend pas une validation humaine
entre deux actions.

## Deux documents, et c'est tout

| Document | Ce qu'il porte | Qui l'écrit |
|---|---|---|
| **`protocole.md`** | Les invariants, le pipeline P0-P7, la boucle de correction, la porte de publication, les cas d'arrêt, la doctrine N1-N11, S1-S8, E1-E12, et les deux tables du contrat de correction | Personne : il se reprend tel quel |
| **Le régime d'autorisation du projet** | Les décisions du propriétaire : pré-autorisation du CLI, création du ticket, publication, et les exceptions aux règles par défaut du protocole | Le projet, une fois. **Une quinzaine de lignes** |

**Ce que le projet ne fournit pas.** Comment on lance, où se lit le verdict, quels canaux de preuve
existent, ce que le contrôle statique ne couvre pas : **l'agent le trouve en regardant**, et le
consigne en P0 dans son relevé d'amorçage. Un projet n'a pas à pré-mâcher ce qu'une exploration
établit.

**Pourquoi cette frontière et pas une autre.** Un document qui pré-répond à « comment on lance »
devient une **synthèse au second degré**, qui vieillit comme toute synthèse -- alors que le protocole
tranche déjà en faveur du code contre la synthèse. Ce qui reste par écrit est ce qui n'existe nulle
part : une permission ne se découvre pas, elle se donne. Et deux des trois décisions ne sont même pas
des documents -- la pré-autorisation est un drapeau de lancement de session.

**Où le mettre.** Dans un fichier court et distinct, à côté de la documentation du projet. Pas
**dans** elle : la dépendance va dans un seul sens. Le régime d'autorisation cite la documentation du
projet ; la documentation du projet n'a pas à connaître le protocole -- elle est lue par des agents
qui font tout autre chose, et doit rester juste si ce protocole n'est pas employé.

## Contenu du paquet

```
etendu/
├── README.md                          ce fichier
├── protocole.md       LE document normatif, indépendant de toute technologie
├── gabarit_prompt_de_demarrage.md     le message qui ouvre une conduite, et ses variantes
├── gabarit_regime_dautorisation.md    une quinzaine de lignes, à écrire une fois par projet
├── gabarit_cadrage.md                 format de l'artefact de P2
├── gabarit_analyse_detaillee.md       format de l'artefact de P4
├── gabarit_plan_implementation.md     format de l'artefact de P5
├── tests/
│   ├── lancer_les_tests.py           la seule commande à passer après tout changement
│   ├── test_porte.py                 quinze cas sur la porte de publication
│   ├── test_sous_sections.py         six cas sur le parseur de fiches
│   └── donnees/plan_fictif.md        document du contrôle positif du contrat
├── verifier_chemins_declares.py       hygiène des chemins du manifeste
├── verifier_contrat_de_correction.py  contrôle indépendant du projet
└── verifier_porte_de_publication.py   la porte, indépendante du projet elle aussi
```

## Se servir du protocole

### Sur un projet neuf

1. **Écrire le régime d'autorisation** à partir de `gabarit_regime_dautorisation.md`, dans un
   fichier court et distinct. Trois décisions, plus les exceptions aux règles par défaut du protocole
   s'il y en a. Une quinzaine de lignes.
2. **Écrire le prompt de démarrage** à partir de `gabarit_prompt_de_demarrage.md`. Quatre pointeurs,
   plus le périmètre du travail. Rien de la méthode, rien des permissions.
3. **Conduire.** Le point d'entrée est `protocole.md`. L'agent réclame lui-même ses
   trois préconditions ; il n'y a rien à lui rappeler.
4. **Publier.** En fin de conduite, l'agent franchit la porte de publication et pousse sa branche. Il
   ne demande rien : c'est la porte qui autorise, pas son appréciation.

### Le prompt de démarrage

Quatre pointeurs, et un seul est propre au protocole.

```text
Applique le protocole spécifié ici : <chemin du protocole>
Le projet est décrit ici : <la documentation du projet, sa synthèse>
L'objet de la tâche est décrit ici : <besoin, analyse, ticket -- une SOURCE, pas une entrée normative>
Ce que le protocole attend de ce dépôt est ici : <le régime d'autorisation>
```

Rien d'autre n'est à dire à l'agent : il réclame lui-même ses trois préconditions, et il consigne en
P0 ce qu'il a trouvé.

**Format complet, variantes et pièges : `gabarit_prompt_de_demarrage.md`.** Il porte le bloc de
délimitation à recopier quand un document préexistant est cité, les variantes -- correction
d'anomalie, conduite partielle, chantier neuf, dispositif de validation payant -- et ce qui ne va
jamais dans un prompt.

### Sur un projet déjà entamé

C'est le cas courant, et il ne demande aucun régime particulier. Deux distinctions suffisent, toutes
deux détaillées dans le protocole, section « Un projet déjà entamé ».

**Le protocole porte un incrément, pas une base de code.** On ne le réapplique jamais à un existant :
on l'applique au prochain incrément, et tout ce qui précède est de l'existant que P1 cartographie. Le
coût est proportionnel à l'incrément, pas à l'historique. Il n'y a donc pas de « protocole à
rattraper » sur un projet en cours.

**Un plan ou une spécification rédigés hors protocole sont des sources, jamais des entrées
normatives.** Ils sont cartographiés en P1 comme n'importe quel document existant, et n'ont aucune
autorité. Conséquence assumée : le plan préexistant sera réécrit. Il sert de source et raccourcit la
cartographie, mais le livrable de P5 est un plan produit sous ce protocole.

**Pourquoi ne pas admettre l'artefact étranger et sauter les phases amont.** Ce serait la voie
apparemment économique, et c'est un faux vert au niveau du processus. Décider qu'un plan étranger est
admissible demanderait de l'auditer, c'est-à-dire de certifier un document dont on ignore les
conditions de production -- au moins aussi cher que refaire l'analyse, et beaucoup moins fiable. Un
plan étranger bien rédigé passerait un tel audit sans porter aucune des garanties qu'il semble
porter.

**Ce qui ne se re-dérive pas : les observations.** Un document se réécrit ; un relevé pris dans des
conditions disparues, non. C'est le seul vrai cas d'héritage, et le protocole lui donne trois
conditions cumulatives avant qu'une observation héritée puisse servir de preuve.

### Vérifier un contrat de correction

```powershell
python verifier_contrat_de_correction.py <chemin_d_un_plan_ou_d_un_cadrage>
```

Le contrôle retourne `EXIT=0` si le document fourni respecte le contrat vérifié.

## Vérifier le paquet

Depuis ce dossier :

```text
python tests/lancer_les_tests.py
```
