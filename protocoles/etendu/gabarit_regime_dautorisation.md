# Gabarit - Régime d'autorisation

## Ce que c'est, et pourquoi c'est court

La **seule** chose que le protocole de quasi-autonomie réclame d'un projet par écrit, avant toute
conduite. Une quinzaine de lignes.

Tout le reste -- comment on lance, où se lit le verdict, quels canaux de preuve existent, ce que le
contrôle statique ne couvre pas -- **l'agent le trouve en regardant**, et le consigne en P0 dans son
relevé d'amorçage. Pré-répondre à ces questions dans un document créé pour l'occasion produirait une
synthèse au second degré, qui vieillirait comme toute synthèse.

Ce qui reste ici est ce qui **n'existe nulle part** : une permission ne se découvre pas, elle se
donne. Et deux des trois décisions ne sont même pas des documents -- la pré-autorisation est un
drapeau de lancement de session.

## Où le mettre : un fichier à lui, et pas ailleurs

**Un fichier court et distinct, à côté de la documentation du projet.** Pas dans la synthèse
d'architecture, pas dans le README.

La raison est une **direction de dépendance**. Le régime d'autorisation cite la documentation du
projet ; la documentation du projet ne doit jamais citer le protocole. Trois conséquences, et chacune
suffirait :

- la documentation d'un projet est lue par des agents qui font tout autre chose -- audit, question,
  exploration -- et à qui le régime d'autorisation ne sert à rien ;
- elle doit rester juste si ce protocole est abandonné, remplacé, ou simplement pas employé sur une
  tâche donnée ;
- **un seul fichier fait foi pour un sujet donné**, et « architecture du projet » n'est pas le même
  sujet que « ce que l'agent a le droit de faire ». Les fondre mélange deux sujets dans un fichier,
  ce que l'invariant I7 interdit.

Le prompt de démarrage porte donc quatre pointeurs distincts : le protocole, la documentation du
projet, la tâche, et ce fichier.

## Trois règles

- **Il se lit, il ne se devine pas.** Une décision qu'il porte ne se tranche jamais par la valeur la
  plus probable.
- **Absent ou muet sur un point nécessaire, c'est un arrêt** -- déclencheur **E12**. L'agent ne le
  complète pas lui-même : il appartient au propriétaire du dépôt.
- **Chaque décision porte sa date.** Elle se retire en modifiant sa ligne, et la date dit depuis
  quand elle vaut.

---

## Gabarit

```markdown
## Régime d'autorisation de l'agent

Décisions du propriétaire du dépôt, <date>. Chacune se retire en modifiant sa ligne.

| Décision | Valeur |
|---|---|
| Pré-autorisation des outils du CLI | <complète, par la commande exacte ; ou liste fermée ; ou aucune> |
| Création du ticket par l'agent | <autorisée, et où vit le mode d'emploi de l'accès ; ou non autorisée> |
| Publication de la branche du sujet | <autorisée derrière la porte du protocole ; ou non autorisée> |

<Risques résiduels acceptés en connaissance de cause, quand la pré-autorisation est complète : ce
que le prompt du CLI protégeait et qui ne l'est plus. Nommer ce qui est propre à ce projet, et pas
seulement les risques génériques.>

### Exceptions aux règles par défaut du protocole

<Une ligne par règle par défaut qui ne tient pas, avec sa raison. Rien si elles conviennent : le
protocole porte déjà une convention de nommage de branche, un préfixe d'instrumentation `releve`, et
les deux tables du contrat de correction.>
```

## Exemple rempli

Relevé sur `chatbot-syrenad`, dans `doc/regime_dautorisation.md`.
egime_dautorisation.md`.

```markdown
## Régime d'autorisation de l'agent

Décisions du propriétaire du dépôt, 2026-08-16. Chacune se retire en modifiant sa ligne.

| Décision | Valeur |
|---|---|
| Pré-autorisation des outils du CLI | Complète, par `claude --dangerously-skip-permissions` |
| Création du ticket par l'agent | Autorisée. Accès GitLab : `<chemin absolu du guide d’accès GitLab installé>`, clé `chatbot-syrenad` |
| Publication de la branche du sujet | Autorisée derrière la porte du protocole |

Risque résiduel accepté, propre à ce projet : la pré-autorisation complète autorise l'agent à
déclencher des appels API payants sans confirmation, et le dépôt en dépend pour deux de ses trois
dispositifs de validation. Il est borné par le protocole et non par l'outil -- toute conduite qui
emploie l'acceptation ou la campagne déclare son nombre de runs dans son cadrage.

### Exceptions aux règles par défaut du protocole

| Règle par défaut | Exception, et pourquoi |
|---|---|
| Nommage de la branche du sujet | La règle par défaut s'applique : `^(feat|fix|docs|chore)/\d+-[a-z0-9-]+$`. L'historique mêle cinq formes -- `issue/16-…`, `feat`, `issue-10`, `1-gestion-images…` -- donc l'agent ne peut pas la relever ; cette ligne la ferme, pour les branches créées après cette date |
```

**Ce que cet exemple montre.** Une seule exception, et elle ne change pas le défaut : elle **confirme**
qu'elle s'applique, parce que l'historique ne permettait pas de le relever. C'est le cas le plus
fréquent : le régime d'autorisation ne dit pas « ma convention est différente », il dit « la
convention n'était pas lisible, voici celle qui vaut ».

## Ce qu'il ne contient jamais

- ce qu'un agent peut trouver en regardant -- commandes, chemins, artefacts, canaux de preuve : cela
  va dans le relevé d'amorçage de P0 ;
- une règle de conception : elle va dans la synthèse du projet, avec le reste de sa doctrine ;
- une règle qui vaudrait pour tout projet : elle appartient au protocole, et sa place s'y discute.
