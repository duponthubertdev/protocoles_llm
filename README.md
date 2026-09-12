# protocoles_llm

Protocoles de développement logiciel avec des agents LLM : compact, standard et étendu,
avec un dispositif de coordination de campagne. Ce dépôt contient leurs gabarits, vérificateurs,
données de test et références nécessaires. Il s’utilise indépendamment de l’atelier personnel.

## Utiliser les protocoles

Partir du [choix des protocoles](protocoles/README.md). Le lanceur choisit le format et fournit
les chemins du protocole, de la documentation du projet, du régime d’autorisation et de la tâche.
Chaque protocole définit ses conditions d’entrée, ses validations et ses conditions d’arrêt.

Conserver l’arborescence du dépôt : les références relatives se résolvent depuis le fichier qui
les cite. Les accès et outils propres au projet traité sont fournis par ce projet.
Aucun fichier d’instructions propre à un fournisseur d’IA n’est nécessaire.

## Références incluses

Les trois protocoles imposent les trois premières références ; la conception renvoie aux deux
compléments spécialisés. Chaque protocole précise quand les consulter.

| Document | Objet |
| :--- | :--- |
| [conception.md](regles/conception.md) | Conception générale |
| [codage.md](regles/codage.md) | Conventions de code et de documentation |
| [conception_de_code_pour_llm.md](llm/conception_de_code_pour_llm.md) | Conception adaptée à l’analyse et à la génération par un LLM |
| [gestion_des_erreurs.md](regles/gestion_des_erreurs.md) | Contrats d’erreur, exceptions et diagnostics |
| [gestion_de_letat.md](regles/gestion_de_letat.md) | État mutable, transitions et coordination |

## Vérifier le paquet

Les vérificateurs et leurs tests utilisent Python 3 et Git, disponibles dans le PATH.
Les imports Python utilisent uniquement la bibliothèque standard et les fichiers de ce dépôt.
Depuis la racine :

```text
python protocoles/standard/tests/lancer_les_tests.py
python protocoles/etendu/tests/lancer_les_tests.py
```

Le compact ne possède pas de vérificateur dédié.
