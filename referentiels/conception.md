# Règles de conception

Ce document s'applique à tous les niveaux : fonction, classe, module, package.

Il est indépendant du langage. Ces règles appliquent les principes de la programmation fonctionnelle indépendamment du langage : immuabilité, fonctions pures, absence d'état partagé, composition et séparation des effets de bord.

## Principe central

Chaque unité de code doit avoir une raison d'exister formulable en une phrase.

## Conception orientée résultat

- Avant toute décision, poser la question : est-ce que cela aide directement à produire le résultat final attendu ?
- Un élément qui ne contribue pas au résultat final est suspect, même s'il semble utile en isolation.
- Les artefacts intermédiaires servent le résultat final ; ils ne sont pas des fins en eux-mêmes et doivent rester régénérables.
- Ne pas construire d'infrastructure pour des artefacts intermédiaires au-delà de ce que le résultat final requiert.

## KISS

- Parmi les solutions qui répondent au besoin réel, choisir la plus simple.
- Ne pas choisir une solution plus générale que le besoin ne l'exige.
- Ne pas transformer une unité de travail en infrastructure.

## DRY

- Ne pas dupliquer une logique : une règle métier, un calcul, une transformation n'existe qu'à un seul endroit.
- Ne pas dupliquer une connaissance : une constante, un format, une contrainte ne se répète pas.
- Si deux endroits doivent changer ensemble, ils partagent probablement une abstraction non encore extraite.

## YAGNI

- Une abstraction non utilisée est de la dette.
- Une option non utilisée est du bruit.
- Un paramètre sans appelant est une promesse non tenue.
- Une fonctionnalité future doit attendre un besoin réel et confirmé.
- Ce qui ne sert pas maintenant est suspect, même si cela semble utile plus tard.

## Responsabilité unique

Chaque unité a une responsabilité unique et formulable clairement.

- **Fonction** : elle calcule, ou elle agit, pas les deux.
- **Classe** : elle représente un concept ou orchestre un flux, pas les deux.
- **Module / package** : il expose une interface cohérente sur un domaine. Si ses membres n'ont pas de raison commune d'être ensemble, le découper.

Quand une unité commence à avoir plusieurs raisons de changer, la découper.

## Cohésion forte et couplage faible

- Cohésion forte : tous les éléments d'une unité concourent à un même objectif. Si les membres d'une classe ou d'un module n'ont pas de raison commune d'être ensemble, découper.
- Couplage faible : minimiser les dépendances entre unités. Une modification dans une unité ne doit pas forcer des modifications en cascade dans d'autres.
- Un couplage fort est souvent le signe d'une abstraction manquante ou d'une responsabilité mal placée.

## Ouvert à l'extension, fermé à la modification (OCP)

- Concevoir une unité pour qu'elle puisse être étendue sans être modifiée lorsqu'un point de variation réel est établi.
- Un point de variation est établi par au moins deux implémentations réelles partageant un contrat stable, ou par une frontière externe qui l'impose : SPI, port ou contrat d'intégration.
- Une variation seulement anticipée est une hypothèse : aucune abstraction n'est introduite, et YAGNI s'applique.
- Quand plusieurs variantes réelles imposent des modifications répétées aux mêmes unités, extraire leur contrat commun au point de variation observé.

## Séparation modèle métier et orchestration

- Un objet métier (`Invoice`, `Order`) peut avoir des méthodes qui opèrent sur ses propres champs (calcul, dérivation, validation interne). Il ne doit pas appeler de repository, de service externe ou d'infrastructure.
- Un service d'application orchestre et appelle l'infrastructure. Il ne doit pas accumuler d'état métier dans ses champs d'instance.
- Quand une classe fait les deux — porte de l'état métier et orchestre des appels externes — la découper en deux responsabilités distinctes.

## Évitement du null

- Ne pas retourner null pour signifier une absence : utiliser Optional, une collection vide ou un type résultat explicite.
- Ne pas accepter null en paramètre : l'appelant résout l'absence avant d'appeler.
- Un null non attendu est un état implicite — le rendre explicite dans le type.

## Immuabilité

- Préférer les valeurs aux références mutables.
- Quand une mutation est inévitable, la rendre atomique : écrire dans une cible temporaire, substituer en une seule opération.

## Fonctions pures

- Écrire des fonctions pures partout où le besoin ne justifie pas d'effet de bord.
- Une fonction pure ne produit aucun effet observable en dehors de sa valeur de retour.
- Mêmes entrées, même sortie. Toujours.

## État borné et explicite

- Déclarer l'état explicitement, ne pas le capturer implicitement.
- Borner l'état à la plus petite unité qui en a besoin.
- Ne modifier l'état que depuis l'unité qui le possède.

Éviter :

- l'état global ou partagé implicitement ;
- les modifications d'état en dehors du composant propriétaire ;
- les effets de bord cachés dans des fonctions qui semblent pures ;
- les dépendances à l'état d'une exécution précédente.

Voir [gestion_de_letat.md](gestion_de_letat.md) pour les transitions, la coordination des mutations
et les tests des composants avec état.

## Functional Core / Imperative Shell

- Le **functional core** contient toute la logique de décision et de transformation. Il reçoit des valeurs, retourne des valeurs, ne lit rien, n'écrit rien, n'appelle aucun service externe.
- Le **imperative shell** lit l'état du monde, appelle le core avec les données extraites, écrit le résultat. Il contient les effets de bord, pas la logique.

## Composabilité et dépendances

- Les dépendances sont déclarées, pas découvertes.
- **Fonction** : les entrées nécessaires sont dans les paramètres.
- **Classe** : les dépendances sont injectées à la construction.
- **Module** : les interfaces importées sont déclarées, pas résolues par convention interne.

Ce qui brise la composabilité :

- capturer des dépendances implicitement (globales, contexte, environnement) ;
- produire des effets de bord en plus de la valeur retournée ;
- supposer un ordre d'initialisation ou d'appel non déclaré ;
- dépendre d'une implémentation concrète au lieu d'une interface.

## Testabilité

- Concevoir chaque unité pour qu'elle soit testable indépendamment.
- Une unité non testable indépendamment a une dépendance implicite ou une responsabilité trop large.
- Ne pas ajouter du code de production dont la seule raison d'exister est d'être appelé par des tests : si une logique n'est pas testable directement, c'est le signe d'un découpage manquant.
- Ne pas rendre public ce qui devrait être privé pour le rendre testable : extraire une classe à la place.
- En Java, la visibilité package-private est l'outil pour tester sans exposer au-delà du module.
- Ne pas tester via reflection.

## Composition

- Assembler des unités simples plutôt que construire une unité complexe.
- Une unité complexe est un signe que plusieurs responsabilités n'ont pas été extraites.
- La composition de fonctions pures est préférable à l'héritage ou à l'état partagé.

## Conception LLM-friendly

Les LLM sont l'outillage principal de développement. Une conception LLM-friendly réduit les hallucinations, améliore la qualité de génération et permet une analyse fiable du code existant.

- **Formuler toute convention comme une règle binaire vérifiable.** Une convention qui demande du jugement pour être appliquée délègue ce jugement à un processus stochastique — elle produit de la variance entre agents et entre sessions. Une règle fermée, sans exception, produit le même comportement à chaque session. L'absolutisme d'une règle n'est pas un défaut : c'est le mécanisme par lequel un LLM devient prévisible sur la durée.
- Garder les unités petites et bornées : une fonction ou classe dont le comportement complet tient dans une fenêtre de contexte réduite est analysable de manière fiable.
- Appliquer des patterns consistants : un LLM prédit la suite la plus probable. Des patterns cohérents dans la base de code réduisent les erreurs de génération.
- Rendre les dépendances explicites : injection de dépendances, absence de globals, Functional Core — tout ce qui rend le contexte d'une unité auto-suffisant évite à l'agent d'inférer un état caché.
- Nommer sans ambiguïté : un nom qui décrit complètement ce que fait l'unité réduit la surface de décision de l'agent lors de la génération et de l'analyse.
- Éviter la magie implicite : conventions cachées, surcharge d'opérateurs non évidente, comportement dépendant de l'ordre d'initialisation — tout ce qu'un agent ne peut pas déduire localement est une source d'erreur.

## Gestion des erreurs

- Catcher aux frontières du système, pas au milieu de la logique. Une exception n'est attrapée que par celui qui peut la traiter.
- Modéliser le type d'erreur dans le contrat : absence légitime → `Optional<T>` ou type résultat explicite ; erreur inattendue → exception typée avec message contextualisé.
- Séparer les erreurs récupérables des erreurs fatales : une erreur récupérable fait partie du contrat de l'interface ; une erreur fatale signale un état incohérent qui ne doit pas être masqué.
- Ne pas avaler une exception pour retourner une valeur neutre : continuer sur une base incorrecte est plus dangereux qu'échouer explicitement.

Voir `gestion_des_erreurs.md` pour la hiérarchie d'exceptions, les messages, le logging et les stratégies de récupération.

## Fail fast

- Signaler les erreurs le plus tôt possible, au niveau le plus proche de la cause.
- Valider à l'entrée d'un composant, pas au milieu de son exécution.
- Un message d'erreur dit ce qui était attendu et ce qui a été constaté.
- Ne pas continuer sur une entrée invalide.
- Ne pas avaler une exception pour retourner une valeur neutre sans signaler le problème.
