# Gabarit - Plan d'implémentation d'une étape

Ce fichier fait foi seul. Il porte à la fois ce que le plan doit accomplir et la forme qu'il prend.

**Le plan fait foi une fois écrit.** L'analyse détaillée est un document de travail, temporaire :
elle sert à produire le plan, puis cesse d'être la référence. Le plan recopie donc intégralement ce
dont l'exécutant a besoin, y compris le code que l'analyse contenait déjà. La duplication est
assumée et voulue : elle évite qu'un exécutant froid ait à ouvrir un second document.

## Objectif

Permettre à un modèle moins performant, démarrant à contexte vide, d'exécuter chaque étape seule,
sans erreur, sans décision stratégique, sans improvisation.

## RP1 - Règles pour les étapes

Un plan est rédigé en markdown et découpé en étapes.

Chaque étape doit :

- être atomique. Une étape peut contenir plusieurs actions si elles sont indissociables pour
  atteindre un état fonctionnel ; sinon, créer des étapes séparées ;
- laisser le code dans un état fonctionnel et testable ;
- se terminer par un test de validation exécutable par l'agent.

Chaque étape doit pouvoir être exécutée par un modèle moins performant démarrant avec un contexte
vide, sans erreur.

L'exécution d'une étape ne doit nécessiter aucune décision stratégique, aucune improvisation, et
aucune connaissance des autres étapes.

Une étape est conçue et écrite avec la même rigueur que du code.

## RP2 - Règles pour le plan

Le plan doit être :

- rédigé selon la contrainte de prose relevée en P0. La contrainte sur les
  identifiants ne
  porte que sur le code et les scripts, pas sur la prose explicative ;
- clair, précis, sans ambiguïté, sans contradiction ;
- sans emoji ni symbole Unicode décoratif : ni flèches, ni coches, ni pictogrammes. Écrire `->`,
  `OK`, `KO` ;
- commencé par une section de contexte en entête, suivie des étapes.

La section de contexte doit contenir le contexte et l'objectif, la structure des répertoires, et les
règles spécifiques au projet.

**Aucune commande git comme étape de travail.** Ce n'est pas parce que git serait manuel : l'agent
commite lui-même, et le protocole lui impose quatre points de commit obligatoires. C'est précisément
pour cela qu'aucune étape ne les rappelle -- ils sont une obligation permanente, énumérée dans « Ce
que l'agent fait avec git », et non une décision de conception à rejouer dans chaque plan. Un plan
qui les recopierait en ferait des étapes optionnelles, puisque toute étape peut être adaptée.

## RP3 - Vérifier les chemins avant de rédiger

Avant de rédiger, vérifier l'existence de tous les chemins référencés : répertoires, fichiers
d'entrée, fichiers de configuration. Un chemin incorrect oblige à corriger le plan en cours
d'exécution et perturbe le modèle exécutant.

## RP4 - Règles pour la validation

**Langage : Python par défaut.** Les scripts de validation sont écrits en Python, sauf contrainte
spécifique rendant Python inadapté. Un langage de script d'interpréteur système pose trop de
problèmes de compatibilité et de lisibilité pour être le choix par défaut.

La section de validation est écrite par le rédacteur du plan et exécutée par l'agent lui-même après
chaque étape. L'agent se valide donc lui-même, ce qui crée un risque de complaisance : il peut
réussir une validation qu'il aurait dû échouer. Les validations doivent être mécaniques, objectives,
et aussi difficiles à contourner que possible.

Cinq contraintes s'appliquent.

**La validation doit échouer si l'action a mal été exécutée.** C'est la contrainte la plus
importante. Avant d'écrire la commande, se demander : cette commande échouerait-elle si l'exécutant
avait inventé le résultat ou produit un fichier vide ? Sont insuffisants : vérifier qu'un fichier
existe sans vérifier son contenu, vérifier qu'une commande s'exécute sans vérifier sa sortie,
vérifier un sous-ensemble trop restreint du résultat attendu.

**Une validation sans cible échoue.** Si la cible que la validation devait examiner est absente, la
validation échoue avec un code non nul. Elle ne retourne jamais « rien à signaler » parce qu'elle n'a
rien trouvé à examiner : c'est un faux vert, et le plus dangereux de tous puisqu'il se présente comme
une preuve. C'est la règle N10 du protocole, appliquée aux validations d'étape.

**Code de sortie : 0 en succès, non nul en échec.** La commande ne doit pas être interactive.

**Erreurs terminantes.** Toute erreur termine le script immédiatement avec un code non nul. Un échec
silencieux est pire qu'un plantage : il laisse croire que la validation a réussi.

**Messages d'erreur : nom du test, valeur attendue, valeur constatée.** Le message est la seule
information disponible pour diagnostiquer. Il doit être lisible sans avoir le plan sous les yeux.

Format obligatoire :

```text
Validation KO -- <contexte> : attendu='<X>', constate='<Y>'
```

Le numéro d'étape est obligatoire dans tout message, échec comme succès :

```text
Etape N -- Validation KO -- <contexte> : attendu='<X>', constate='<Y>'
Etape N OK
```

Toute validation lisant une sortie structurée doit s'appuyer sur des chemins de propriétés
confirmés. Ne jamais supposer la structure.

**Un discriminant se prouve sur les deux états.** Une validation qui sépare deux états -- réussi ou
repris, présent ou absent, vide ou rempli -- doit être éprouvée sur les deux, ou son discriminant
doit être confronté à un témoin connu de l'état opposé. Une sous-chaîne cherchée dans un artefact
généré est particulièrement suspecte : feuilles de style, gabarits et en-têtes contiennent souvent le
mot que l'on croit discriminant. Coût de la vérification : quelques secondes sur un artefact déjà
disponible. Coût de son absence : une validation qui ne peut jamais passer, découverte après une
exécution complète.

**Une validation qui exécute l'action ne peut pas être rejouée.** Si la validation déclenche
elle-même le traitement qu'elle vérifie, la moindre correction du critère impose de tout réexécuter.
Séparer : l'action déclenche, la validation constate sur l'artefact produit. La validation doit alors
s'assurer qu'elle examine bien le bon artefact, et non le plus récent venu.

Renseigner la section Prérequis dès que la validation vérifie l'existence d'un fichier : un agent
faible peut terminer l'action sans avoir produit le fichier attendu.

## RP5 - Tests sur données réelles

Quand des fichiers de référence sont disponibles, la dernière validation doit inclure un test de
bout en bout sur des copies de ces fichiers. Ne jamais exécuter sur les fichiers de référence
eux-mêmes. Supprimer les copies en fin de validation, dans le même script. Vérifier la sortie
produite, pas seulement le code de sortie.

## RP6 - Continuité entre étapes

Si une étape produit une valeur technique exacte qu'une étape ultérieure devra réutiliser -- chemin,
version, nom de variable, résultat de commande :

- l'action doit demander d'écrire cette valeur dans un fichier dédié, avec une clé nommée
  explicitement ;
- l'étape suivante doit la relire explicitement depuis ce fichier. Ne pas supposer que l'agent s'en
  souvient ;
- la validation doit vérifier mécaniquement que la clé est présente et non vide.

Ne pas appliquer si la valeur n'est utilisée que dans la même étape.

## RP7 - Contexte d'exécution

Le plan est exécuté par un seul agent, en session unique. Il exécute les étapes dans l'ordre, valide
chaque étape avant la suivante, et s'arrête en cas d'échec.

Conséquences : chaque étape est autonome ; ne pas supposer que l'agent se souvient des étapes
précédentes, préférer des références explicites aux fichiers produits ; la section de validation est
vue par l'agent avant qu'il n'exécute l'action, donc n'y mettre aucune information qui influencerait
l'exécution.

## RP8 - Style

Clair, bref, concis. Sacrifier la grammaire au profit de la concision. Le style télégraphique est
admis.

## RP9 - Ambiguïté résiduelle

Si une question se pose pendant la rédaction, c'est que l'analyse détaillée n'a pas satisfait son
exigence d'absence de décision résiduelle. La conduite à tenir dépend de la nature du manque :

- **manque d'information factuelle** : compléter l'analyse en observant ou en lisant le code, puis
  reprendre la rédaction. Ne pas trancher dans le plan ce que l'analyse aurait dû trancher ;
- **déclencheur d'escalade** au sens du protocole : arrêter, écrire le constat, et attendre une
  décision
  de l'utilisateur.

Ne jamais lever une ambiguïté par une formulation prudente dans le plan : l'exécutant la lirait
comme une décision déjà prise.

Cette règle remplace la liste de questions posées une à une à l'utilisateur, qui suppose une
présence humaine à chaque étape de rédaction.

## RP10 - Conduite après un échec, recopiée dans le plan

Le plan doit porter, en entête et avant la première étape, le **bloc canonique** du protocole,
délimité par ses deux marqueurs `<!-- CONTRAT DE CORRECTION : DEBUT -->` et
`<!-- CONTRAT DE CORRECTION : FIN -->`, marqueurs exclus. Il s'ouvre sur le titre « Conduite à tenir
quand une validation échoue ».

**Il se recopie tel quel, sans reformulation, sans ajout et sans retrait.** Adapter le bloc est
interdit, ses deux tables comprises. Un renvoi ne suffit pas : le plan a déclaré à l'exécutant qu'il
n'avait aucun autre document à ouvrir.

**La doctrine qui entoure le bloc dans le protocole ne se recopie pas.** Elle explique pourquoi le
dispositif est ce qu'il est, ce qui sert à le maintenir et non à décider au moment d'un échec. C'est
la raison d'être des marqueurs : « recopier la section » demandait de juger ce qui relevait du
contrat, et une convention qui exige du jugement produit de la variance.

Sans cette section, l'exécutant connaît le format de la fiche de KO mais ignore quelle classe
autorise quelle modification, quand s'arrêter, et ce qu'il n'a jamais le droit de faire. Il
improvise, et l'improvisation après un échec est exactement la défaillance que le protocole traite.

**Il n'y a pas de liste de contenu à vérifier.** Le bloc porte tout ce que l'exécutant doit avoir
sous les yeux -- la distinction entre l'action mal exécutée et l'échec réel, la règle d'ordre de la
fiche, les deux tables, les interdits, le plafond, l'autorisation d'instrumenter, les cas d'arrêt en
toutes lettres, et la phrase qui dit qu'un arrêt n'est pas un échec. Énumérer ce contenu ici
rétablirait le tri que les marqueurs suppriment, et divergerait du bloc à la première évolution.

**Une seule chose s'ajoute autour du bloc**, et elle ne s'y trouve pas : ce que l'exécutant consigne
en plus de la fiche -- frictions et écarts dans le bilan, observations dans le référentiel relevé en
P0, au moment où ils surviennent.

Les codes de déclencheurs d'escalade du protocole ne sont pas repris tels quels dans le plan : un
exécutant froid n'a pas la table des codes. Les cas d'arrêt s'y écrivent en clair.

**Cette recopie est vérifiée par script.** `verifier_contrat_de_correction.py` cherche les marqueurs
du contrat dans le fichier déclaré sous la clé **`contrat_de_correction`** du manifeste, et échoue si
l'un manque. Un plan amputé de cette section ne passe pas le contrôle statique, quel que soit l'état
du code livré.

**Quand il n'y a pas de plan, cette règle ne disparaît pas, elle se déplace.** Une conduite partielle
sans P5 -- une mesure, une observation -- n'écrit aucun plan mais agit quand même. Le contrat est
alors porté par le **cadrage**, et c'est lui que le manifeste déclare sous la même clé : elle nomme
le rôle, pas le type d'artefact. Voir `gabarit_cadrage.md`, section conditionnelle « Conduite à tenir
quand une validation échoue ». Le contrat n'est jamais recopié aux deux endroits : un seul fichier
fait foi pour un sujet donné.

## RP11 - Avant de rédiger

Annoncer explicitement l'état de préparation. Soit les questions restantes, soit la phrase :
« Je n'ai pas de question, je suis prêt à rédiger le plan. »

---

## Structure du plan

### Section de contexte, en entête

- **Contexte et objectif** : ce que l'étape livre, en trois à cinq lignes.
- **Structure des répertoires** : où vivent les artefacts touchés.
- **Règles spécifiques** : uniquement celles que l'exécutant risque d'enfreindre sur cette étape.
  Les rappeler ensuite dans les étapes concernées, au plus près de l'action.
- **Périmètre d'écriture autorisé** : liste plate et exhaustive des chemins absolus. Tout fichier
  hors de cette liste est en lecture seule. Un besoin d'en sortir est un déclencheur d'escalade, pas
  une décision d'exécution.
- **Devoir permanent** : ce que l'exécutant doit consigner en parallèle des étapes, indépendamment
  de leur succès. Frictions et écarts dans le bilan, observations dans le référentiel désigné par le
  le relevé d'amorçage de P0, au moment où ils surviennent.

### Section « Conduite à tenir quand une validation échoue », avant la première étape

Recopiée depuis le protocole, selon RP10. Aucune étape ne doit décrire sa propre
procédure de correction : les étapes renvoient à cette section unique.

### Template d'étape

```markdown
### Étape N : Titre court

**Entrées :** fichiers ou données nécessaires, ou "aucune"

**Contexte :** fichier ou fonction concernée, ou "--"

**Pourquoi :** objectif de l'étape

**Action :** ce qu'il faut faire exactement

**Pièges :** contraintes ou cas limites propres à cette étape -- omettre si aucun

**Prérequis :** fichier ou état qui doit exister avant la validation -- omettre si l'action ne
produit pas de fichier

**Validation :**
```python
# script exécutable par l'agent
```
```

### Section « Notes d'exécution », en fin de plan

Obligatoire. Vide à la rédaction, alimentée pendant l'exécution, dès qu'un écart survient et sans
attendre la fin.

Elle porte les écarts au plan, les validations KO, les pièges rencontrés non documentés, et les
décisions prises en cours d'exécution.

**Elle est aussi le journal des KO du protocole.** Une entrée est écrite **avant** toute
modification consécutive à un échec, jamais après : écrite après, elle justifierait ce qui a déjà
été fait au lieu de décider ce qu'il faut faire.

Format d'une entrée :

```markdown
### Étape N -- <titre court de l'événement>

**Statut :** OUVERTE

**Symptôme :** ce qui a échoué, recopié depuis l'artefact, pas reformulé.

**Preuves :** chemins absolus et lignes.

**Le comportement observé est-il conforme au cas d'utilisation ?** oui ou non, et sur quelle preuve.

**Hypothèse :** une seule, réfutable.

**Contre-indication :** le fait qui écarterait cette hypothèse.

**Classe :** une des classes de KO de la table du protocole.

**Surface d'écriture autorisée :** chemins absolus, ou "aucune" avec le code d'escalade.

**Tentative :** 1 ou 2. À 3, arrêt obligatoire.

**Cause :** ce qui a provoqué l'écart.

**Correction :** ce qui a été fait, ou "aucune, escalade".

**Résultat :** résultat de l'exécution suivante, avec le chemin absolu de son artefact.
```

**Le champ `Statut` est obligatoire, et sa valeur est fermée : `OUVERTE` ou `CLOSE`.** Il vaut
`OUVERTE` à l'écriture de la fiche, et passe à `CLOSE` quand le résultat est connu. Ce n'est pas une
redondance avec le champ `Résultat` : celui-ci est une phrase, que rien ne permet de contrôler, alors
que le statut est vérifié par la porte de publication, qui refuse de publier une branche dont une
fiche reste ouverte -- ou ne déclare aucun statut.

Une fiche close par un **arrêt** porte `CLOSE` dès que la décision du propriétaire du dépôt est
consignée, même si la ligne concernée reste bloquée : ce que le statut décrit est la fiche, pas la
ligne.
