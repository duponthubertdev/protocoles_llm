# Développer avec des agents LLM

**Des protocoles prêts à donner aux agents pour préparer, coder et vérifier vos évolutions et correctifs.**
Vous récupérez les changements, les preuves de validation et les limites restantes, selon un
référentiel de qualité adaptable. Ce sont des documents et des contrôles à utiliser avec votre
outil d'IA habituel, sans service à installer ni fournisseur imposé.

## Pour commencer

- **Git et Python 3**, accessibles dans le terminal. Les contrôles Python n'utilisent aucune dépendance externe.
- **Un outil d'IA capable de lire et modifier des fichiers et d'exécuter des commandes**, avec accès à votre projet et à ce dépôt cloné.
- **L'environnement de développement et de test de votre projet**, et une documentation qui le présente, par exemple son README.

Dans les prompts, remplacez `<protocoles>` et `<projet>` par les **chemins absolus** des dépôts,
et `README.md` par votre documentation. Conservez l'arborescence de ce dépôt.

Préparez les autorisations une fois. Cet exemple garde la publication à votre charge :

```text
Prépare <projet>/doc/regime_dautorisation_standard.md à partir du modèle
« Régime d'autorisation » dans <protocoles>/protocoles/standard/protocole.md.
Le projet est décrit dans <projet>/README.md.
Mes décisions : lecture, modification des fichiers du périmètre, commandes
locales de build et de test, création d'une branche de sujet et commits autorisés.
Création de tickets et publication non autorisées. Convention de branche :
celle du protocole. Aucune exception aux référentiels.
Relève le nom de la branche principale dans Git. Je lancerai moi-même
les exécutants ; aucun lancement d'exécutant n'est délégué à l'orchestrateur.
```

Relisez ce fichier et configurez les permissions de votre outil d'IA en accord avec vos décisions.

## 1. Un travail : vous et un exécutant

L'exécutant est l'agent qui réalise le travail. Ouvrez une session dans votre projet.
Le protocole **standard** lui fera préparer, implémenter et vérifier ce correctif :

```text
Applique le protocole spécifié ici :
<protocoles>/protocoles/standard/protocole.md

Le projet est décrit ici :
<projet>/README.md

Le régime d'autorisation propre au protocole standard est ici :
<projet>/doc/regime_dautorisation_standard.md

La tâche :
Corriger l'export CSV : un champ contenant le séparateur crée actuellement
une colonne supplémentaire à la relecture. Préserver les valeurs et le nombre
de colonnes, y compris avec des guillemets ou des retours à la ligne dans un champ.
Conserver le séparateur et l'encodage actuels.
```

**L'agent analyse, planifie, corrige et teste**, sans que vous ayez à demander chaque étape.
Il vous sollicite pour les décisions qui vous appartiennent. Vous examinez ensuite le diff,
les validations et les limites de son bilan, puis décidez de fusionner.

## 2. Plusieurs travaux : ajoutez un orchestrateur

L'orchestrateur prépare et suit l'ensemble dans **une session distincte**, sans coder. Chaque travail
confié à un exécutant est une *conduite* ; l'ensemble forme une *campagne*. Exemple : une recherche
côté serveur, puis son interface. Commencez par demander à l'orchestrateur :

```text
Le projet est décrit dans <projet>/README.md.
Je veux rechercher les produits par leur nom depuis la liste affichée.
La recherche ignore la casse ; une saisie vide affiche la liste habituelle.

Prépare <projet>/doc/cadrage_campagne_recherche.md à partir de :
<protocoles>/protocoles/campagne/gabarit_cadrage.md
Prévois deux travaux : la recherche côté serveur, puis son intégration
à l'interface. Propose les critères de réception de l'ensemble.
Présente-moi les questions à trancher et le cadrage avant toute implémentation.
```

Après vos réponses et votre validation du cadrage, poursuivez dans cette même session :

```text
Orchestre la campagne décrite ici :
<projet>/doc/cadrage_campagne_recherche.md

Les protocoles disponibles et leur règle de sélection sont décrits ici :
<protocoles>/protocoles/README.md

Le projet et son régime d'autorisation sont décrits ici :
<projet>/README.md
<projet>/doc/regime_dautorisation_standard.md

Pour cette campagne, utiliser le standard pour chaque conduite.
Tu n'exécutes toi-même aucune conduite. Prépare le message de lancement
de chaque exécutant ; je l'enverrai dans une nouvelle session.
Après chaque conduite, vérifie son résultat et ses preuves, puis mets
à jour le cadrage avant de poursuivre. N'ajoute aucun travail hors de
l'objectif fixé. Vérifie aussi le résultat d'ensemble avant de clore la campagne.
```

**Vous copiez le prompt fourni dans une nouvelle session d'exécutant**, puis rapportez son bilan
à l'orchestrateur. Celui-ci vérifie le résultat avant de préparer le travail suivant.
Vous décidez des fusions entre les travaux dépendants.

**À l'arrivée : une fonctionnalité vérifiée de bout en bout, avec un code conçu pour rester simple,
lisible et testable.** Un obstacle non résolu reste signalé ; des tests verts ne garantissent pas toute la qualité.

## Adapter à votre équipe

- **Le format** : [standard](protocoles/standard/protocole.md) pour structurer le travail ; [compact](protocoles/compact/protocole.md) pour un besoin déjà cadré, avec un seul document. Voir les [critères de choix](protocoles/README.md).
- **La qualité** : forkez le dépôt et adaptez les [référentiels](referentiels/) de conception et de codage à votre équipe.
- **La coordination** : réutilisez les [gabarits de campagne](protocoles/campagne/README.md). Vous pouvez autoriser le lancement automatique des exécutants si votre outil le permet.

Pour vérifier les outils fournis, depuis la racine de ce dépôt :

```text
python protocoles/standard/tests/lancer_les_tests.py
```

Cette suite teste le vérificateur du standard, pas votre application. Le compact n'a pas de
vérificateur dédié ; les deux formats exigent des contrôles exécutables du travail livré.
