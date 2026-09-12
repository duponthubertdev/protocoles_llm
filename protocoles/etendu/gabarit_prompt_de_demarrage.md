# Gabarit - Prompt de démarrage

## Ce que c'est

Le message qui ouvre une conduite. Il ne contient **que des pointeurs et le périmètre du travail** :
tout ce qui relève de la méthode vit dans le protocole, tout ce qui relève des permissions vit dans
le régime d'autorisation du dépôt.

Quatre pointeurs, et un seul est propre au protocole.

| Pointeur | Ce qu'il désigne | Ce qui se passe s'il manque |
|---|---|---|
| Le protocole | La méthode | L'agent improvise la méthode |
| La documentation du projet | Le système sur lequel on travaille | L'agent explore à l'aveugle, et paie une cartographie qui existait |
| L'objet de la tâche | Ce qu'il faut faire, et son périmètre | L'agent choisit le périmètre |
| Le régime d'autorisation | Ce que le propriétaire a décidé | Arrêt **E12** dès l'amorçage |

Les pointeurs de contexte viennent d'abord, la tâche en dernier : l'instruction actionnable est ainsi
la plus proche de l'exécution.

## Gabarit

```text
Applique le protocole spécifié ici :
  <chemin du protocole.md>

Le projet est décrit ici :
  <chemin de la documentation du projet, sa synthèse d'architecture>

Ce que le protocole attend de ce dépôt est ici :
  <chemin du régime d'autorisation>

L'objet de la tâche est spécifié par <ce document | ces documents | ce ticket> :
  <chemins absolus ou URL HTTPS du ticket>

<Le bloc de délimitation, ci-dessous : obligatoire dès qu'un document préexistant est cité.>

<Les variantes applicables, ci-dessous.>
```

## Le bloc de délimitation, quand un document préexistant est cité

À recopier tel quel. Il porte la seule ambiguïté que ce prompt puisse créer.

```text
Ils délimitent le travail : ne pas élargir le périmètre, ne pas traiter un autre
sujet. Leur contenu est une source à vérifier — une contradiction avec le code se
tranche en faveur du code.

Conduis les premières phases du protocole pour les convertir en artefacts
conformes, puis exécute la suite à partir des artefacts convertis, jamais des
documents d'origine.
```

**Pourquoi ces deux paragraphes plutôt qu'un.** Le premier dit ce que le document *fait* — il
délimite — et ce qu'il *n'est pas* — une autorité factuelle. Le second dit ce qu'on en fait : on le
convertit, on ne l'exécute pas. Sans le second, un agent bloqué en P6 retourne naturellement lire le
document d'origine plutôt que celui qu'il a produit, et récupère au passage ce que la conversion
avait corrigé.

## Variantes

### Correction d'anomalie

```text
C'est une correction d'anomalie : P0 doit établir une preuve rouge préalable.
```

Ajouter, quand le document préexistant confond un filet de caractérisation avec une preuve rouge --
cas fréquent, parce qu'un filet est vert par construction :

```text
Le <artefact> du plan d'origine est vert par construction : ce n'est pas une
preuve rouge.
```

Cette phrase transforme un blocage prévisible en décision déjà prise, plutôt qu'en découverte
coûteuse à P6.

### Conduite partielle

```text
Phases <liste> seulement : <raison pour chaque phase omise>.
```

Une mesure, une observation, une investigation ne livrent aucun code : P5 et P6 sont sans objet. Le
protocole l'autorise, mais la conduite doit l'annoncer -- et P0, les connaissances préalables et le
contrat de correction restent dus.

### Chantier neuf, aucun document préexistant

Retirer le pointeur « objet de la tâche » et le bloc de délimitation, et les remplacer par le besoin
en une à trois lignes, ou par l'URL HTTPS du ticket. Rien d'autre ne change.

### Coût d'exécution non négligeable

Quand le projet valide par un dispositif payant -- appels à une API facturée, environnement partagé,
temps machine long :

```text
Déclare dans le cadrage le nombre d'exécutions de <dispositif> que la conduite
emploiera, avant d'en lancer une.
```

## Ce qui ne va jamais dans un prompt de démarrage

**Une formule qui accorde une autorité factuelle à un document.** « Source de vérité » en est
l'exemple type : elle se lit comme une dispense de vérification, et le défaut qu'elle produit est
invisible puisque la vérification est précisément ce qui aura été sauté. Si le propriétaire veut
réellement dispenser de vérifier, c'est une décision : elle vit dans le régime d'autorisation, datée
et motivée. Un prompt s'écrit vite et ne se relit pas.

**Une permission.** Pré-autorisation, création de ticket, publication : régime d'autorisation.

**Une règle de méthode.** Elle appartient au protocole, et sa place s'y discute. Un prompt qui
contredit le protocole ne le remplace pas -- voir « Quand le prompt de démarrage contredit le
protocole ».

**Ce que l'agent trouvera en regardant.** Commandes, chemins, canaux de preuve, angles morts du
contrôle statique : cela se relève en P0. Un prompt qui les pré-remplit crée une source périmable de
plus.

## Exemple rempli

Employé sur `chatbot-syrenad` le 2026-08-16.

```text
Applique le protocole spécifié ici :
  <chemin absolu du protocole étendu installé>

Le projet est décrit ici :
  C:\Users\hdupo\git\chatbot-syrenad\synthese.md

Ce que le protocole attend de ce dépôt est ici :
  C:\Users\hdupo\git\chatbot-syrenad\doc\regime_dautorisation.md

L'objet de la tâche est spécifié par ces deux documents :
  C:\Users\hdupo\git\chatbot-syrenad\doc\projets\erreur_diagnostique\analyse_diagnostic_erreur_fournisseur.md
  C:\Users\hdupo\git\chatbot-syrenad\doc\projets\erreur_diagnostique\plan_diagnostic_erreur_fournisseur.md

Ils délimitent le travail : ne pas élargir le périmètre, ne pas traiter un autre
sujet. Leur contenu est une source à vérifier — une contradiction avec le code se
tranche en faveur du code.

Conduis les premières phases du protocole pour les convertir en artefacts
conformes, puis exécute la suite à partir des artefacts convertis, jamais des
documents d'origine.

C'est une correction d'anomalie : P0 doit établir une preuve rouge préalable. Le
« filet de caractérisation » de l'étape 1 du plan d'origine est vert par
construction — ce n'est pas une preuve rouge.
```

## Avant de lancer

Trois vérifications qui coûtent une minute et évitent un arrêt en fin de conduite.

- **Les chemins cités existent.** Un pointeur cassé se découvre à l'amorçage, mais un rangement
  récent en casse plusieurs à la fois.
- **Le ticket éventuel est accessible.** Sinon, la conduite s'arrêtera avant P0.
- **L'arbre de travail est propre**, ou du moins ses fichiers suivis modifiés sont rangés. La porte
  de publication refuse tout fichier suivi modifié hors du périmètre déclaré : l'arrêt tomberait une
  fois tout le travail fait.
