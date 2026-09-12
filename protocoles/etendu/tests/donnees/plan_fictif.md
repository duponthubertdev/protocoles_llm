# Plan fictif — contrôle du contrat de correction

Document de test : il sert de contrôle positif au vérificateur du contrat de correction.
Il ne constitue pas un gabarit de plan complet.

## Conduite à tenir quand une validation échoue

**Un arrêt n'est pas un échec de l'exécutant.** C'est le comportement attendu, et il est préférable à
une correction hasardeuse. Un agent qui veut bien faire peut s'obstiner, et l'obstination est
exactement ce que ce dispositif cherche à empêcher.

### Deux situations à ne pas confondre

**L'action n'a pas été exécutée comme écrite.** Fichier oublié, contenu tronqué, faute de frappe. On
refait l'action et on relance la validation. Ce n'est pas un échec, et cela ne demande aucune fiche.

**L'action a été exécutée comme écrite et la validation échoue quand même.** C'est un échec réel, et
il déclenche intégralement la procédure ci-dessous.

### La fiche s'écrit avant toute écriture

Avant toute écriture consécutive à un échec réel, écrire une fiche dans la
section « Notes d'exécution » du document portant le contrat, au format fixé par le gabarit de plan
d'implémentation. La fiche répond à :

> Le comportement observé est-il conforme à ce que le cas d'utilisation décrit ?

| Constat | Qui a tort | Conséquence |
|---|---|---|
| Le système produit un résultat cohérent avec l'intention, l'attendu de la validation est absent ou différent | La validation | Corriger l'attendu |
| L'effet produit est observable, mais diffère de la lettre du cas d'utilisation | La rédaction du cas d'utilisation | Ajuster l'oracle à l'effet réel et documenter l'écart |
| Aucun effet observable, ou effet contraire à l'intention métier | Le comportement applicatif | **Arrêt, aucune correction** |
| Le dispositif ne trouve pas ce qu'une observation prouve présent | La désignation employée -- sélecteur, chemin, clé, identifiant | Corriger la désignation, après nouvelle observation |
| Le dispositif fait autre chose que ce que le scénario décrit | Le scénario | Corriger le scénario |
| La donnée nécessaire n'a jamais été produite | Le producteur de la donnée | Corriger le producteur, ou **arrêt** |
| Un résultat varie sans qu'aucune modification l'explique | Rien n'est établi | **Se mesure, ne se corrige pas** |

La frontière entre « la rédaction a tort » et « le comportement applicatif a tort » est l'existence
d'un **effet observable**. Un cas d'utilisation est une description humaine, jamais parfaite : un
écart de forme s'absorbe en ajustant l'oracle. Seule l'absence d'effet, ou un effet contraire à
l'intention métier, bloque.

### Surface d'écriture autorisée

Pendant la correction, la surface est **celle qu'a déclarée le document portant le contrat**, ni plus
ni moins. Un fichier préexistant que ce document autorise à modifier reste modifiable ; un fichier
qu'il n'a pas déclaré est en lecture seule, même s'il a été créé par la conduite.

| Classe du KO | Surface autorisée, dans les limites du périmètre déclaré |
|---|---|
| Attendu faux | L'artefact qui porte l'attendu |
| Désignation fausse | L'artefact qui porte la désignation, après nouvelle observation |
| Scénario faux | L'artefact qui porte le scénario |
| Production mal construite | L'artefact qui décrit la production de la donnée |
| Donnée absente ou producteur en échec | Aucune -- arrêt |
| Comportement applicatif divergent | Aucune -- arrêt |
| Défaut hors périmètre déclaré | Aucune -- arrêt |
| Validation fausse | Aucune -- arrêt |
| Variation inexpliquée | Aucune -- à mesurer séparément |

La classe du KO restreint la **nature** du fichier modifiable ; le périmètre déclaré en restreint la
**liste**. Les deux s'appliquent.

### Les interdits

- aucune attente ajoutée qui ne soit une intention nommée adossée à un témoin déclaré ;
- aucune reprise locale, aucune pause fixe, aucune action par contournement technique, aucune action
  par index ;
- aucune extension d'une abstraction existante pour absorber un cas particulier.

Un quatrième prime sur les trois autres : **ne jamais modifier une validation pour la faire passer.**
Un agent bloqué peut toujours affaiblir son propre critère de succès, et c'est la sortie la plus
tentante puisqu'elle réussit à coup sûr. Une validation affaiblie transforme un échec bruyant en faux
vert silencieux.

Si une validation paraît elle-même fausse, c'est un cas d'arrêt, pas une invitation à la corriger.

### Instrumenter reste autorisé

La table des surfaces borne les **corrections**. Elle ne borne pas l'observation : un agent bloqué a
le droit de poser une instrumentation de diagnostic temporaire, y compris en créant un artefact neuf,
quelle que soit la classe du KO.

Conditions : l'artefact porte le préfixe `releve` ; sa règle de retrait est écrite avant son code ;
il ne porte aucune assertion et ne corrige rien ; il ne compte pas dans le plafond.

### Le plafond

**Deux tentatives sur le même symptôme.** À la troisième, arrêt, quel que soit le niveau de
conviction.

### Cas d'arrêt immédiat

L'agent s'arrête, écrit le constat avec ses preuves, et attend une décision.

- une anomalie de la source d'exigences touche le périmètre traité ;
- un cas d'utilisation n'est pas spécifié, ou l'est de façon non exécutable ;
- aucune donnée productible ne permet d'exercer le comportement à vérifier ;
- l'environnement, un compte ou un droit nécessaire n'est pas disponible ;
- l'action ne produit aucun effet observable, ou l'effet observé contredit l'intention métier -- une
  simple imprécision de rédaction du cas d'utilisation n'est pas un cas d'arrêt ;
- corriger un échec imposerait de modifier un fichier hors du périmètre autorisé ;
- une décision nécessaire contredit un choix déjà livré antérieurement ;
- deux tentatives de correction sur le même symptôme ont échoué ;
- une observation nécessaire est impossible à obtenir ;
- une validation paraît elle-même fausse ;
- poursuivre exigerait une opération de destruction ou une publication engageante ;
- le régime d'autorisation du dépôt est absent, ou ne tranche pas une autorisation nécessaire à la poursuite.

**La portée d'un arrêt est celle de ce qu'il bloque, et rien de plus.** Par défaut c'est la ligne
concernée, et tout le reste du périmètre continue. Élargir un arrêt au-delà de ce qu'il bloque est
une faute symétrique de celle de poursuivre malgré lui : bloquer tout un périmètre au premier
obstacle se présente comme de la prudence, et coûte plus cher.

Dans tous les cas, le document final dit explicitement ce qui a été livré et ce qui ne l'a pas été.

### Une variation inexpliquée se mesure

Un symptôme qui apparaît puis disparaît sans qu'aucune modification l'explique n'entre dans aucune
ligne de la table des surfaces. Il arrête **la ligne concernée, jamais la conduite**, et se classe
avec, au minimum : les deux populations d'observations contradictoires et le nombre de passages de
chacune, la preuve que le code et les données étaient identiques entre elles, et le constat qu'aucune
correction opportuniste n'a été appliquée entre-temps.

La mesure devient un travail distinct, proposé et non exécuté.

### Reprise après un arrêt

Un arrêt n'est pas une fin. Le chemin est le même pour tous les cas d'arrêt.

1. Écrire la fiche, s'arrêter, et exposer le constat avec ses preuves et, s'il y en a une, la
   correction proposée **sans l'appliquer**.
2. Le propriétaire du dépôt décide : correction validée, autre approche, ou abandon de la ligne.
3. Si la correction est validée, l'appliquer. La lacune qui a conduit à l'arrêt reste consignée dans
   la fiche ; le propriétaire décide si elle justifie une évolution du protocole. Une faute ponctuelle
   dans un script ne justifie pas une règle générale.
4. **Reprendre à l'étape minimale suffisante, jamais depuis le début.** Corriger une validation
   reprend à cette validation seule ; corriger une valeur observée reprend à l'observation qui l'a
   produite ; corriger une décision de conception reprend à l'analyse.
5. Clore la fiche par son résultat.

## Notes d'exécution

Aucun échec.
