La priorité est la maintenabilité et la documentation du code.

# Principes directeurs

- Maintenabilité — c'est la priorité absolue.
- LLM friendly : noms auto-décrivants, patterns consistants, abstractions justifiées, commentaires avec exemples.
- Minimiser les risques de désynchronisation entre composants.
- Convention over configuration.

# Commentaires

Commenter le code en faisant un effort particulier pour expliquer les intentions, les choix de conception et les parties non évidentes.

Les commentaires doivent être clairs, concis et à jour avec le code.

# Conventions de codage

Le code doit être au maximum auto-explicatif, avec des noms clairs et descriptifs même s'ils sont un peu longs.

Respecter les conventions et le style de code existant dans le projet. La cohérence est plus importante que les préférences personnelles.

Le code doit se lire plus comme une recette de cuisine que comme un théorème mathématique.

**Symboles du programme** — identifiants, noms de fonctions, constantes, clés techniques, chaînes utilisées comme données par le code (clés de map, noms de colonnes, arguments CLI) : ASCII pur.

**Messages techniques** — logs, stderr, messages d'erreur diagnostiques, sorties structurées destinées à être parsées ou traitées par un outil : ASCII pur.

**Prose incorporée** — commentaires, docstrings, messages affichés en langage naturel à l'utilisateur (libellés de menu, guidance, textes d'aide) : français avec accents.

Le critère : ce qui peut apparaître dans un log, une trace ou être traité par un outil → ASCII ; ce qui est uniquement affiché à l'écran en langage naturel → accents.

**Emoji et symboles Unicode décoratifs : interdits partout**, dans le code comme dans la prose. Sont interdits : emoji (✅, ⚠️, 🎉), flèches Unicode (→, ⇒, ←), symboles de dessin (└──, ├──), coches et croix (✓, ✗). Utiliser à la place : `->` ou des mots pour les flèches, `-` ou l'indentation pour l'arborescence, `OK`/`KO` pour les statuts.

# Conventions Git

Toute modification d'un élément versionné doit se faire sur une branche dédiée dont le nom suit les bonnes pratiques de nommage.

Une branche ne doit contenir que des modifications cohérentes avec ce qui a initié sa création.

Chaque commit doit avoir une unité conceptuelle.

# Conventions de nommage

## Modules et namespaces

Un module ou namespace doit nommer son domaine de façon explicite. Tous les éléments qu'il contient partagent une responsabilité commune et identifiable.

- Si tu ne peux pas formuler cette responsabilité en une phrase courte : c'est un fourre-tout — éclate-le.
- Si tu peux la formuler mais que le nom ne la reflète pas : renomme-le.

Les noms `outils`, `utils`, `helpers`, `commun` sont des signaux d'alerte fréquents, pas une liste exhaustive d'interdits.

## Types et fonctions

- Type avec état ou comportement propre : nom de domaine seul. Exemple : `Registre`, `Onglet`, `InterrupteurConnexion`.
- Regroupement de fonctions utilitaires sans état : suffixe `Utils`. Exemple : `DateUtils`, `StringUtils`, `JacksonUtils`.
- Aucun préfixe d'entreprise (`Ns`, `Syr`, etc.).

## Variables

- Nom court si le type est visible dans les 10 lignes précédentes.
- Nom descriptif sinon.
- Ne pas répéter le nom du type dans le nom de la variable : préférer `suite` plutôt que `configSuite`.

## Documentation

Obligatoire sur tout type et toute fonction, publique ou privée.

Le commentaire doit ajouter au moins une information que le nom et la signature ne donnent pas : cas limite, contrainte de contrat, pourquoi architectural, précision de comportement.

Un commentaire qui ne fait que reformuler le nom est du bruit — reformuler le nom plutôt qu'écrire un tel commentaire.

Expliquer le POURQUOI et les contraintes, pas le QUOI que le code dit déjà.

Format natif du langage. En français avec accents.
