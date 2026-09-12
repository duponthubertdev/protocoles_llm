# Les trois protocoles - lequel employer

Trois méthodes de conduite d'une évolution par un agent LLM. Elles sont **indépendantes** : chacune
se lit et s'applique seule, aucune n'en cite une autre, et un agent ne passe jamais de l'une à
l'autre en cours de route.

Une **conduite** est un travail délimité, mené selon un protocole, de son ouverture à sa clôture
ou à son arrêt. Le **document de conduite** en conserve l’état, les décisions et les résultats.

Une livraison composée de plusieurs conduites peut être regroupée dans une **campagne** définie par
le propriétaire. L'orchestrateur choisit et nomme le protocole de chaque conduite sans jamais en
changer pendant son exécution. Voir `campagne/README.md`.

**Le choix appartient à celui qui lance la conduite, jamais à l'agent qui l'exécute.** Il est nommé
dans le message d'ouverture, et rien d'autre ne le désigne. Un agent qui choisirait sa méthode se
donnerait aussi le droit d'en changer quand elle le gêne.

## Les formats

Compact, standard et étendu désignent l’organisation du travail, avec les mêmes exigences de qualité.

| Format | Organisation et conditions d’emploi |
| :--- | :--- |
| `compact` | Un document de conduite ; travail déjà cadré ; attendu vérifiable automatiquement. |
| `standard` | Quatre documents ; attendu vérifiable automatiquement ; choix par défaut. |
| `etendu` | Établissement formalisé de l’état initial, dossier d’audit détaillé ou contrôle mécanique de publication. |
| `campagne` | Coordination de plusieurs conduites, chacune avec son protocole désigné. |

## Les critères de choix

Les trois formats exigent un attendu vérifiable automatiquement. Un contrôle peut être créé pendant
la conduite : l'absence actuelle d'un test n'est pas l'absence d'un oracle. Si aucun contrôle
pertinent ne peut être défini, l'exécutant rend la main. Une acceptation humaine nécessaire et
non couverte par les contrôles reste en attente.

| Préparation et dispositifs nécessaires | Protocole |
| :--- | :--- |
| Besoin, limites et critères d'acceptation déjà établis ; préparation consignée dans un document unique | `compact` |
| Cadrage à établir et travail à structurer en observations, analyse et plan | `standard` |
| Un dispositif supplémentaire décrit ci-dessous est nécessaire | `etendu` |

Le choix appartient au lanceur. Un travail déjà cadré peut rester sous standard si son organisation
en quatre documents est souhaitée ; l'exécutant ne change pas de format.

## Quand choisir l'étendu

Le standard est le choix par défaut pour un attendu vérifiable automatiquement, même si un
compactage est probable. Choisir l'étendu lorsqu'un besoin explicite impose l'un de ses dispositifs :

1. **Établissement formalisé de l'état initial d'un chantier existant** : baseline, cartographie
   et manifeste.
2. **Dossier d'audit détaillé** : cadrage, faits, analyse, plan et validations dans des artefacts
   distincts.
3. **Contrôle mécanique de publication de la branche** : la porte
   `verifier_porte_de_publication.py` confronte l'état du dépôt au périmètre déclaré. La publication
   reste soumise au régime d'autorisation.

La durée, la difficulté du diagnostic et le risque de compactage ne suffisent pas à choisir
l'étendu. Le dispositif supplémentaire nécessaire est nommé au lancement lors du choix du protocole.

## Les dispositifs

| | compact | standard | étendu |
| :--- | :--- | :--- | :--- |
| Documents produits | 1 | 4 | ~8 plus un manifeste |
| Pas | 5 | 8 | 8 phases, P0 à P7 |
| Contrôle mécanique dédié | aucun -- historique Git examiné par l'exécutant | `verifier_documents.py` | trois scripts |
| Relecture des sources avant écriture | oui | oui | oui |
| L'agent peut publier sa branche | selon le régime d'autorisation | selon le régime d'autorisation et les conditions de clôture | selon le régime d'autorisation et après passage de la porte |
| Lignes à lire avant de commencer | ~350 | ~580 | ~1 500 |

## Ce qui vaut pour les trois

- **La même exigence de conception greenfield** s'applique aux évolutions et aux corrections,
  sans élargir les autorisations ni modifier le traitement des anomalies ou les conditions d'arrêt.
- **Les mêmes trois référentiels** de conception et de codage s'appliquent, imposés par chaque
  protocole et lus avant le premier pas.
- **Le projet ne fournit qu'une chose écrite d'avance : le régime d'autorisation.** Chaque protocole
  lit **le sien**, jamais celui d'un autre. Un régime absent, ou muet sur un point nécessaire, est
  un arrêt.
- **Le travail vit sur une branche du sujet**, jamais sur une branche principale.
- **L'agent ne se donne pas ce qu'il n'a pas reçu** : ni permission, ni méthode, ni périmètre.

**Limite face au compactage du contexte.** La relecture des sources avant écriture ne protège pas
contre la perte de l’état d’exécution, notamment la répétition d’un test déjà effectué. Si ce
problème est constaté, le propriétaire peut décider d’étendre la relecture à l’état d’avancement
avant les exécutions concernées. Cette extension n’est pas activée par défaut.

## Le message qui ouvre une conduite

Chaque protocole porte le sien, en fin de document, et il ne s'improvise pas. Il ne contient que
quatre choses : le chemin du protocole, celui de la documentation du projet, celui du régime
d'autorisation, et la tâche.

Rien d'autre n'y entre -- pas de règle de méthode, pas de permission, et aucune formule qui donne
autorité à un document.
