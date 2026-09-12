# Règles de gestion des erreurs

Ce document complète `conception.md` (section `## Gestion des erreurs`).

Il s'applique à tous les langages. Les exemples sont en Java et Python.

## Classification des erreurs

Toute erreur appartient à exactement une catégorie.

| Catégorie | Définition | Mécanisme |
| --- | --- | --- |
| Absence légitime | Résultat valide où l'élément cherché n'existe pas. Ce n'est pas une erreur. | `Optional<T>`, valeur sentinelle, liste vide |
| Erreur récupérable | Condition prévue dans le contrat, que l'appelant doit gérer. | Exception checkée (Java), type résultat (`Result<T,E>`) |
| Erreur fatale | État incohérent ou violation de contrat non récupérable à ce niveau. | Exception non checkée, propagation jusqu'à la frontière |
| Erreur de programmation | Bug : précondition violée, argument invalide, état impossible. | Assertion, exception non checkée, fail fast immédiat |

Ne pas utiliser une exception pour signaler une absence légitime.

Ne pas utiliser une valeur neutre (null, -1, "") pour masquer une erreur fatale.

## Où catcher

- Catcher uniquement là où l'erreur peut être traitée : corriger, compenser, ou produire un message utile à l'utilisateur.
- Ne pas catcher pour relancher immédiatement sans ajout de contexte.
- Ne pas catcher dans la logique métier une exception d'infrastructure (I/O, réseau) : la laisser remonter jusqu'à la frontière du système.
- Les frontières du système (point d'entrée CLI, contrôleur HTTP, handler de tâche) sont les endroits naturels pour catcher, logger et produire un message utilisateur.

## Modélisation des erreurs

### Java

- Absence légitime : `Optional<T>`. Forcer l'appelant à gérer le cas vide dans le type.
- Erreur récupérable prévue : exception checkée avec nom métier (`AnalyseIntrouvableException`, `FichierManquantException`).
- Erreur fatale non récupérable : `RuntimeException` ou sous-classe non checkée.
- Ne pas créer une exception custom si une exception standard suffit (`IllegalArgumentException`, `IllegalStateException`).

### Python

- Absence légitime : retourner `None` uniquement si le contrat le documente explicitement, ou utiliser un type union (`T | None`).
- Erreur récupérable : exception custom héritant de `Exception`, nommée par le domaine.
- Erreur de programmation : `ValueError`, `TypeError`, `AssertionError`.
- Ne pas retourner `None` sans documenter que `None` est un résultat valide.

## Hiérarchie d'exceptions

- Nommer les exceptions par leur cause métier, pas par leur mécanisme technique : `GroupeIntrouvableException` plutôt que `LookupException`.
- Créer une exception custom uniquement si l'appelant a besoin de la distinguer d'une autre exception pour la traiter différemment.
- Une hiérarchie d'exceptions doit pouvoir être décrite par un arbre de causes métier, pas par un arbre de mécanismes.
- Ne pas créer une exception par module ou par classe par convention : créer une exception quand le besoin de distinction existe.

## Messages d'erreur

- Format : `attendu='<valeur attendue>' constate='<valeur constatée>'`.
- Le message doit permettre de corriger le problème sans lire le code source.
- Inclure le contexte : chemin de fichier, identifiant de l'objet concerné, valeur reçue.
- Ne pas écrire `"Erreur inattendue"`, `"Échec"`, `"KO"` seuls sans contexte.
- Les messages d'erreur sont des messages techniques : ASCII pur (voir `codage.md`).

Exemples :

```python
# Mauvais
raise ValueError("Fichier invalide")

# Bon
raise ValueError(f"fichier_manquant: attendu='{chemin}' constate='absent'")
```

```java
// Mauvais
throw new RuntimeException("Erreur");

// Bon
throw new GroupeIntrouvableException(
    "groupe_introuvable: attendu='" + idGroupe + "' constate='absent dans groupes_fonctionnalites.csv'"
);
```

## Propagation vs récupération

- Laisser remonter ce qu'on ne peut pas traiter. Ne pas attraper pour relancher.
- Ajouter du contexte à une exception avant de la relancer : wrapper avec le contexte manquant.
- Ne pas transformer une erreur fatale en erreur récupérable pour simplifier le code de l'appelant.
- Ne jamais continuer le traitement après une erreur non récupérable dans l'espoir que la suite compense.

## Logging des erreurs

- Logger à la frontière du système, pas à chaque niveau de propagation. Une erreur loggée plusieurs fois produit du bruit.
- Niveau `ERROR` : erreur qui empêche l'action attendue de se terminer.
- Niveau `WARNING` : condition anormale mais récupérable, traitement qui continue.
- Niveau `INFO` : jalons du flux normal utiles au diagnostic.
- Ne pas logger une exception puis la relancer sans ajout : choisir l'un ou l'autre.
- Le message de log suit le même format que le message d'exception : contexte + attendu/constaté.

## Tests des chemins d'erreur

- Tester les chemins d'erreur aussi rigoureusement que les chemins nominaux.
- Vérifier le type de l'exception, pas seulement qu'une exception est levée.
- Vérifier le message de l'exception quand il porte une information contractuelle.
- Un test qui attrape `Exception` sans vérifier le type ne teste rien.

## Cas particuliers

### Partial failure

- Un traitement qui échoue partiellement doit signaler l'échec, pas retourner un résultat partiel silencieux.
- Si l'agrégation d'erreurs apporte de la valeur (lister tous les IDs invalides d'un lot), l'expliciter dans le contrat et documenter le format de retour.
- Ne pas mélanger résultats valides et erreurs dans la même structure sans le documenter.

### Ressources et nettoyage

- Garantir la libération des ressources même en cas d'erreur : `try/finally`, `with`, `try-with-resources`.
- Ne pas avaler l'exception dans le bloc `finally`.

### Erreurs dans les constructeurs

- Un constructeur qui échoue sur une précondition lève une exception immédiatement.
- Ne pas construire un objet dans un état invalide et laisser l'erreur se manifester plus tard.
