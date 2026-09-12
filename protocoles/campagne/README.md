# Coordination de campagne

Une campagne regroupe les conduites que le propriétaire place sous un même objectif de livraison.
Elle orchestre les protocoles ; elle ne les remplace pas et n'en modifie aucun.

## Règles

1. Le propriétaire fixe l'objectif et les tâches de la campagne.
2. L'orchestrateur transforme chaque tâche en une conduite au périmètre fermé, choisit son protocole et le nomme avant son lancement.
3. Chaque exécutant applique un seul protocole pendant toute sa conduite.
4. Après chaque conduite, l'orchestrateur contrôle son artefact de clôture et les preuves auxquelles il renvoie, puis met à jour le cadrage.
5. Le régime d'autorisation du projet détermine si l'orchestrateur peut lancer un exécutant sans nouvel accord. Aucun exécutant n'est lancé si ce droit n'y est pas tranché.

Le cadrage conserve seulement l'état nécessaire pour choisir la prochaine conduite et juger la livraison. Les détails d'exécution restent dans les bilans des conduites.
Une conduite `bloquee` porte une condition de reprise vérifiable. La validation de l'objectif de livraison est un acte distinct : elle ne se déduit pas des verdicts individuels.

## Utilisation

1. Créer `cadrage_campagne_<theme>.md` à partir de `gabarit_cadrage.md`.
2. Lancer l'orchestrateur avec `gabarit_prompt.md`.
3. Clore la campagne lorsqu'aucune conduite n'est `a_faire` ni `en_cours` et que l'objectif de livraison a été vérifié.
