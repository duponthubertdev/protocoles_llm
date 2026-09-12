# Théorie : écrire du code LLM-friendly

Ce document explique comment concevoir du code pour faciliter son analyse et sa génération
par un LLM. « Pour LLM » désigne cette adaptation au modèle ; l’accès au code et l’exécution
passent par le harnais, logiciel qui organise les outils et les échanges. L’ensemble forme l’agent.

---

## Le modèle et son accès au code

Le LLM traite le contenu que le harnais lui transmet dans sa fenêtre de contexte.
Le harnais est le logiciel qui organise les échanges, expose les outils au modèle et fait
exécuter les appels autorisés. L’agent désigne le système constitué du modèle et de ce harnais.

L’accès aux fichiers, la recherche, l’indexation et la navigation dépendent des outils
du harnais. Une capacité disponible dans l’environnement n’est pas nécessairement utilisée,
et une information accessible n’est pas nécessairement présente dans le contexte du modèle.

Les recommandations de ce document visent à rendre les informations utiles faciles à trouver
et à transmettre, puis compréhensibles dans le contexte effectivement fourni au modèle.
Elles ne supposent pas que tous les environnements sont dépourvus de navigation ou d’indexation.

---

## 0. Réduire la variance : le principe fondamental

### Pourquoi

Un LLM est non-déterministe non seulement au sein d'une session, mais entre sessions froides,
entre agents, entre versions de modèle. La même question posée à froid deux semaines plus tard
peut produire une réponse différente.

Toute zone grise dans les conventions est une source de variance qui s'accumule. Le jour 1,
un agent choisit le package `vue.fluent`. Le jour 30, avec un contexte différent, un autre
agent choisit `vue`. Sans qu'aucun des deux n'ait commis d'erreur, la base de code devient
incohérente — produit de la variance probabiliste, pas d'une faute humaine.

### Conséquence directe : l'absolutisme est une fonctionnalité

Une convention qui exige du jugement pour être appliquée délègue ce jugement à un processus
stochastique. Sur la durée et entre agents, elle produit de la variance et de l'incohérence.

Une règle binaire, vérifiable, sans exception, produit le même comportement à chaque session.
L'absolutisme d'une règle n'est pas un défaut — c'est le mécanisme par lequel un LLM devient
prévisible sur la durée.

Ce principe explique pourquoi toutes les autres règles de ce document sont formulées aussi
fermées que possible. Une règle avec exceptions demande au LLM de juger si l'exception
s'applique — ce jugement est une nouvelle source de variance.

### Exemples

| Convention avec jugement | Convention fermée |
|---|---|
| "Utiliser `@param` quand c'est utile" | "Aucun `@param`" |
| "Mettre la classe dans le package le plus logique" | Règle de dépendance vérifiable par grep |
| "Nommer distinctement sauf si la surcharge est naturelle" | "Jamais de surcharge à contrats différents" |
| "Commenter si non-évident" | "Un exemple Javadoc self-contained sur toute méthode publique non-triviale" |

Dans chaque cas, la convention fermée produit moins de variance entre agents et entre sessions,
au prix d'une légère perte de nuance. Ce compromis est favorable dans un contexte LLM : la
nuance perdue est faible, la cohérence gagnée est forte.

### La règle

Formuler toute convention comme une règle binaire vérifiable. Si une convention nécessite
du jugement pour décider si elle s'applique, c'est un signal pour la reformuler en règle
fermée ou pour la supprimer.

### Limite : préserver la capacité de supervision humaine

Le développeur humain reste dans la boucle pour valider l'output du LLM. C'est ce qui
distingue un système fiable d'une automatisation aveugle.

Si l'organisation du code est trop étrangère aux conventions humaines, le développeur perd
sa capacité de supervision : il ne peut plus distinguer "correct mais non-conventionnel" de
"incorrect". Le superviseur devient aveugle. La fiabilité du système entier diminue, même si
celle du LLM isolément augmente.

Le seuil pratique : pousser les conventions LLM-first aussi loin que possible, sans franchir
le seuil de compréhensibilité pour un développeur familier du projet. Pas nécessairement
conventionnel — compréhensible.

Cette limite est le seul contre-poids au principe de variance. En deçà du seuil, LLM-first
l'emporte. Au-delà, le gain en cohérence LLM est annulé par la perte de supervision humaine.

---

## 1. Les noms doivent être auto-décrivants

### Pourquoi

Dans un IDE, survoler `Champ` affiche sa documentation. Un LLM ne peut pas faire ça.
Il doit déduire le rôle d'un type depuis son nom seul, ou aller lire son fichier source.

Si le nom dit ce que la chose est, le LLM n'a pas besoin d'aller lire le fichier source.
Moins de fichiers à lire = moins de tokens consommés = moins d'erreurs.

### Conséquences pratiques

- `ChampTableau` dit ce que c'est. `Champ` ne le dit pas.
- `construireLaDefinition` dit ce que ça fait. `build` ne le dit pas.
- `obtenirLaListe` dit qu'on obtient quelque chose de type liste. `get` ne dit rien.
- `SeleniumUtils` dit que c'est un regroupement de fonctions utilitaires pour Selenium.
  `Utils` seul ne dit rien sur le domaine.

Les noms longs sont acceptés si lisibles. Un LLM ne fait pas de fautes de frappe — la longueur
du nom n'est pas un obstacle pour lui comme elle l'est pour un humain qui tape au clavier.

---

## 2. Les classes courtes et cohésives sont plus LLM-friendly que les classes monolithes

### L'intuition fausse : "tout dans une classe pour les LLMs"

On pourrait croire que mettre toutes les opérations dans une seule classe (`BasePage`) facilite
le travail du LLM : il n'a qu'un seul endroit à regarder, il trouve tout en un coup.

C'est faux. Voici pourquoi.

### Pourquoi c'est faux

Un LLM qui lit une classe de 450 lignes avec 30+ méthodes doit :
1. Consommer beaucoup de tokens pour lire le fichier entier
2. Filtrer mentalement les méthodes pertinentes parmi celles qui ne le sont pas
3. Maintenir en contexte une surface d'API large, ce qui augmente le risque de confusion

Un LLM qui lit deux classes de 200 lignes chacune, chacune avec une responsabilité claire :
1. Lit uniquement ce dont il a besoin
2. Trouve l'information dense et pertinente
3. Peut raisonner sur chaque classe indépendamment

La taille de la fenêtre de contexte est une ressource limitée. Une classe courte reste entièrement
dans la fenêtre. Une classe longue peut en dépasser les bords, causant des oublis silencieux.

### La découverte par type

Un LLM raisonne sur les types. Si `page.obtenirLaListe("nom")` retourne `ChampTableau`,
le LLM sait qu'il doit lire `ChampTableau` pour connaître les opérations disponibles.

C'est plus efficace que de parcourir 30 méthodes sur `BasePage` pour trouver celles
qui concernent les tableaux. Le type est un pointeur direct vers la bonne classe.

---

## 3. Les patterns consistants réduisent les erreurs de génération

### Pourquoi

Un LLM apprend les patterns à partir des exemples qu'il voit dans le code.
Si un pattern est consistant, le LLM peut le généraliser avec confiance.
Si des exceptions brisent le pattern, le LLM doit les traiter comme des cas spéciaux,
ce qui augmente la probabilité d'erreur.

### Exemple

Dans ce projet, le pattern fondamental est :
```
obtenir un champ depuis la page → agir sur le champ
```

```java
page.obtenirLeChamp("Bouton valider")         // obtenir
    // puis actionner via cliquer() sur la page

page.obtenirLaListe("Liste des demandes")      // obtenir
    .chercherLaLigneEtCliquer(driver, 2, ...); // agir sur le champ
```

Si certaines opérations respectent ce pattern et d'autres non, le LLM doit mémoriser
les exceptions. Plus d'exceptions = plus d'opportunités d'erreur.

Un pattern consistant appliqué partout permet au LLM de généraliser : pour toute nouvelle
opération, il sait qu'il faut d'abord obtenir le champ puis agir dessus.

---

## 4. La Javadoc avec exemples complets est critique

### Pourquoi

Dans un IDE, l'autocomplétion propose les méthodes disponibles au fur et à mesure que
l'utilisateur tape. Il découvre progressivement ce qui existe.

Un LLM ne bénéficie pas de ce mécanisme. Il doit savoir d'avance ce qui existe
et comment l'utiliser. Sa seule source d'information, sans lire le code source entier,
c'est la Javadoc.

Une Javadoc absente ou partielle pousse le LLM à improviser. Il génère ce qui lui semble
plausible d'après le nom de la méthode — ce qui produit du code qui compile parfois mais
est sémantiquement incorrect.

### Ce qu'une bonne Javadoc doit contenir pour un LLM

1. **Le POURQUOI** : dans quel contexte utiliser cette méthode, quand la préférer à une autre
2. **Les contraintes** : ce qui peut lever une exception, les prérequis, les cas limites
3. **Un exemple complet et self-contained** : une invocation concrète, copiable telle quelle,
   qui ne référence pas une variable définie dans la prose au-dessus. Si l'exemple nécessite
   un contexte préalable, ce contexte doit figurer dans l'exemple lui-même.

Les LLMs suivent les exemples avec une précision remarquable. Un exemple dans la Javadoc
est la forme la plus efficace de documentation pour un LLM.

### Ce qu'une mauvaise Javadoc fait

Une Javadoc qui répète le nom de la méthode en prose ("Cherche la ligne et clique dessus")
n'apporte rien. Un LLM lit déjà le nom. Ce qu'il ne peut pas déduire du nom, c'est le
contexte d'utilisation, les prérequis et les cas d'erreur.

Un exemple qui dit `// voir l'appel précédent` ou qui référence une variable non définie
dans l'exemple est également inutilisable : le LLM qui colle l'exemple dans un nouveau
contexte se retrouve avec du code incomplet.

### Règle sur les tags `@param` et `@throws`

#### `@param` : jamais — les contraintes vont dans la prose

Quand une Javadoc est transmise comme extrait textuel, le modèle dispose des éléments
présents dans cet extrait. Une navigation supplémentaire dépend des outils du harnais.
La convention ci-dessous rassemble les contraintes dans la prose pour que le commentaire
soit exploitable sans devoir naviguer entre des tags et une signature fournie ailleurs.

**Règle unique : aucun `@param`.** Les contraintes non-évidentes (contrat null, format,
unité, invariant, base d'index) vont dans le corps du commentaire.

Exemple : au lieu de
```java
@param momentTentative horodatage HH:mm:ss.SSS capture pendant le run
```
écrire dans la prose :
```
{@code momentTentative} doit être au format HH:mm:ss.SSS et capturé pendant le run —
ne pas l'appeler dans {@code generateReport()}, où il serait identique pour toutes
les tentatives.
```

Un `@param` qui reformule le nom ou le type (`@param driver le WebDriver courant`,
`@param dureeMs durée en millisecondes`) est du bruit — le LLM lit déjà la signature.
Le supprimer sans remplacer : si le nom dit déjà tout, aucune documentation n'est nécessaire.

#### `@throws` : sélectif est acceptable, contrairement à `@param`

Chaque exception est une condition indépendante. Un `@throws` absent ne crée pas d'ambiguïté
sur les autres exceptions taguées — le LLM interprète correctement "celle-ci a une condition
non-évidente, les autres sont documentées dans la prose ou évidentes depuis le nom."

Deux sous-règles :
- **Supprimer** un `@throws` si la condition est déjà entièrement décrite dans la prose.
  Exemple : si le commentaire dit "Lève `FooException` si X", le `@throws FooException si X`
  est un doublon — l'un des deux suffit, et la prose est préférable car elle s'intègre
  naturellement à la lecture linéaire.
- **Garder** un `@throws` quand la condition est non-évidente et absente de la prose, ou
  quand l'exception est checked (Java oblige à la déclarer, le tag guide le caller).
  Exemple : `@throws ArrayIndexOutOfBoundsException si tailleDuFiltre dépasse la taille du
  tableau` — la condition ne se déduit pas du nom du paramètre.

---

## 5. Les messages d'erreur explicites facilitent le diagnostic par un LLM

### Pourquoi

Quand le harnais fait exécuter du code et qu’une erreur survient, il peut transmettre
le message d’erreur au LLM pour le diagnostic. Un message vague comme `"Erreur inattendue"` est inutilisable.
Un message du format `"attendu='X', constaté='Y'"` lui permet de corriger sans intervention humaine.

Ce principe s'applique aux exceptions, aux assertions et aux logs.

### Conséquence

Les `catch` silencieux sont particulièrement néfastes dans un contexte d'utilisation par un LLM :
l'exception est avalée, le LLM continue sur une base erronée, l'erreur se manifeste plus tard
dans un contexte déconnecté de la cause réelle.

`fail fast, fail loud` n'est pas seulement une bonne pratique de code — c'est une exigence
pour que les LLMs puissent diagnostiquer et corriger de façon autonome.

### Rendre les contrats explicites dans les types

Un message d'erreur n'est utile qu'après l'erreur. Mieux : rendre le contrat visible dans
le type avant même l'exécution.

Quand une méthode peut ne rien retourner, `Optional<T>` le dit dans le type. Un LLM qui
voit `Ligne trouverUneLigne(...)` peut supposer que la méthode retourne toujours quelque chose
et omettre la gestion du cas absent. `Optional<Ligne>` impose la gestion du cas absent
sans Javadoc supplémentaire — le compilateur l'enforce.

```java
// A eviter -- le LLM peut oublier de tester null
Ligne trouverUneLigne(WebDriver driver, ChampDeColonne... filtre)

// Preferer -- le contrat "peut etre absent" est dans le type
Optional<Ligne> trouverUneLigne(WebDriver driver, ChampDeColonne... filtre)
```

Les types expressifs sont une forme de documentation que ni le LLM ni l'humain ne peuvent
ignorer : le compilateur l'enforce.

### `Optional<T>` vs exception typée : choisir selon la sémantique de l'absence

`Optional<T>` et une exception typée rendent toutes deux le contrat explicite, mais elles
ne disent pas la même chose :

- **`Optional<T>`** : l'absence est un résultat **légitime**. L'appelant doit gérer les deux
  cas. Exemple : chercher un utilisateur dans une base — ne pas le trouver est une issue normale.

- **Exception typée** : l'absence est toujours une **erreur**. Ne pas trouver signifie que
  les données de test sont incorrectes, que l'UI n'est pas dans l'état attendu, ou qu'un bug
  s'est produit. Exemple : `chercherUneLigne` dans un test automation — si la ligne n'est pas
  là, c'est toujours un problème à corriger, jamais un cas à gérer silencieusement.

```java
// Optional -- absence legitime, l'appelant doit traiter les deux cas
Optional<Utilisateur> trouverParLogin(String login)

// Exception typee -- absence = erreur, message explicite avec le contexte
Ligne chercherUneLigne(WebDriver driver, ChampDeColonne... filtre)
// leve LigneIntrouvableException("Aucune ligne trouvee dans 'Liste' pour le filtre : [...]")
```

Dans un contexte de test automation, la plupart des "non trouvé" sont des erreurs.
Utiliser `Optional` forcerait chaque appelant à ajouter `.orElseThrow()` partout, ce qui
est verbeux sans apporter de clarté. L'exception typée avec un message explicite donne
un meilleur diagnostic au LLM : il voit immédiatement ce qui n'a pas été trouvé et pourquoi.

---

## 6. ASCII ou accents : symboles du programme vs prose incorporée

### Pourquoi

Les LLMs tokenisent le texte avant de le traiter. Les caractères accentués produisent
des tokens différents selon les encodages et les tokeniseurs.

Dans les **symboles du programme** — identifiants, noms de fonctions, constantes, clés
techniques, chaînes utilisées comme données par le code (clés de map, noms de colonnes,
arguments CLI) — les accents créent des risques d'encodage, de portabilité et de
compatibilité outillage. La règle est ASCII pur.

Dans les **messages techniques** — logs, stderr, messages d'erreur diagnostiques, sorties
structurées destinées à être parsées ou traitées par un outil — le même risque s'applique.
La règle est ASCII pur.

Dans la **prose incorporée** — commentaires, docstrings, messages affichés en langage
naturel à l'utilisateur (libellés de menu, guidance, textes d'aide) — les accents sont
non seulement acceptés mais requis.

Le critère : ce qui peut apparaître dans un log, une trace ou être traité par un outil
→ ASCII ; ce qui est uniquement affiché à l'écran en langage naturel → accents.

La règle est donc :
- **Symboles du programme** : ASCII pur
- **Messages techniques** : ASCII pur
- **Prose incorporée** : accents requis

### Emoji et symboles Unicode décoratifs : interdits partout

Cette interdiction est distincte de la règle compilateur/prose — elle ne concerne pas l'encodage mais la lisibilité et la stabilité du rendu. La frontière "spécial/standard" étant trop floue pour une règle fiable, on énumère les catégories interdites :

- Emoji : ✅, ⚠️, 🎉, etc.
- Flèches Unicode : →, ⇒, ←, etc. — écrire `->` ou des mots
- Symboles de dessin : └──, ├──, etc. — utiliser l'indentation et `-`
- Coches et croix : ✓, ✗ — écrire `OK`/`KO`

Un LLM ne peut pas déduire de façon fiable ce qui est "spécial" sans liste. Une règle sur "caractères spéciaux" sera interprétée différemment à chaque génération. Une liste avec exemples est la seule forme qui résiste à l'ambiguïté.

---

## 7. Les paramètres explicites plutôt que l'état implicite

### Le cas `driver`

Dans les méthodes tableau migrées sur `ChampTableau`, le `WebDriver` est passé en paramètre
explicite. Dans la version `BasePage`, il était implicite (stocké comme champ).

La version implicite semble plus pratique (moins à écrire), mais la version explicite est
plus LLM-friendly. Voici pourquoi.

Quand un LLM génère un appel de méthode, il voit la signature : `chercherLaLigneEtCliquer(WebDriver driver, int index, ...)`.
Le paramètre `driver` est dans la signature — le LLM sait qu'il doit le passer.

Avec l'état implicite (`BasePage` stocke le driver), le LLM doit savoir que le driver
est déjà disponible dans l'objet. S'il génère une nouvelle classe ou un nouveau contexte,
il peut oublier d'initialiser le driver ou le passer au mauvais endroit.

L'explicite est plus verbeux mais sans ambiguïté. Pour un LLM, l'absence d'ambiguïté
prime sur la concision.

### Mitigation de la friction

Le coût de friction lié aux paramètres explicites dans les classes internes est absorbé par
la facade fine (voir §10) : la facade stocke le `driver` en champ, et le passe explicitement
aux classes internes dans chaque délégation d'une ligne. Le LLM qui écrit un test ne voit
que la facade sans paramètre — le LLM qui maintient la logique interne voit des signatures
claires. Les deux niveaux sont ainsi optimisés indépendamment.

La mitigation supplémentaire : un exemple Javadoc montre toujours le pattern complet,
incluant comment obtenir le `driver`. Le LLM suit l'exemple.

---

## 8. Éviter les abstractions spéculatives

### Pourquoi

Les abstractions créées "pour le futur" ou "au cas où" produisent des couches intermédiaires
qui n'ont pas de nom métier clair. Un LLM qui rencontre une couche d'indirection sans
sémantique propre doit dépenser des tokens à comprendre son rôle.

Les abstractions justifiées par un besoin réel et documenté (avec Javadoc) sont prévisibles.
Les abstractions spéculatives ajoutent du bruit sans valeur.

YAGNI ("You Aren't Gonna Need It") est encore plus important dans un contexte LLM que dans
un contexte humain, parce que chaque couche supplémentaire est une source de confusion
potentielle pour le LLM.

---

## 9. La constante nommée plutôt que la valeur magique

### Pourquoi

```java
champ.actionner(driver, "x");         // Que signifie "x" ?
champ.actionner(driver, ChampCliquable.CLIQUER);   // "CLIQUER" dit ce que ça fait
```

Un LLM qui génère un appel d'action sur un champ cliquable doit savoir quelle valeur passer.
Si la valeur est `"x"`, il doit avoir vu cet usage dans un exemple pour le reproduire.
Si la valeur est `ChampCliquable.CLIQUER`, il peut le déduire du type `ChampCliquable`
et du nom de la constante, sans avoir vu d'exemple.

Les constantes nommées sont de la documentation inline exploitable par un LLM.

---

## 10. Le pattern Facade fine : un point d'entrée sans graisse

### L'intuition "tout dans une classe" — partiellement juste

L'intuition "mettre toutes les opérations dans une seule classe pour que le LLM n'ait qu'un
endroit à regarder" n'est pas totalement fausse. Elle pointe vers un besoin réel : quand un
LLM écrit un test, il ne devrait pas avoir à connaître dix classes différentes. Trop de classes
à consulter = trop de contexte à charger = plus d'erreurs.

Le problème est que cette intuition est souvent mise en oeuvre comme une **facade grasse** :
une classe qui contient à la fois l'interface publique ET toute la logique. Résultat : la classe
grossit sans limite, noie le signal dans le bruit, et redevient difficile à utiliser.

### La bonne réponse : la facade fine

Une **facade fine** fournit le point d'entrée unique sans contenir la logique :

```java
// BasePage (facade fine) -- le LLM ne lit que ce fichier pour ecrire un test
public <T extends BasePage> T chercherLaLigneEtCliquer(
        String nomListe, int index, ChampDeColonne... filtre) {
    obtenirLaListe(nomListe).chercherLaLigneEtCliquer(driver, index, filtre);
    return (T) this;
}

// ChampTableau -- la logique est ici, le LLM n'a pas besoin de le savoir pour ecrire un test
public void chercherLaLigneEtCliquer(WebDriver driver, int index, ChampDeColonne... filtre) {
    // implementation reelle
}
```

Le LLM qui écrit un test ne lit que `BasePage`. La logique est dans `ChampTableau`, mais
c'est transparent pour lui. Si un LLM doit maintenir ou déboguer la logique, il lit
`ChampTableau` directement — la responsabilité est dans le bon endroit.

La facade stocke le `driver` en champ et le passe en paramètre explicite aux classes internes
dans chaque délégation. Cela résout la tension décrite en §7 : les classes internes ont des
signatures explicites sans que le LLM qui écrit un test soit exposé à cette friction.

### Les trois cas et leur LLM-friendliness

| Pattern | LLM-friendliness | Pourquoi |
|---|---|---|
| Facade grasse (tout dans une classe, logique incluse) | Mauvaise | Classe trop grande, bruit élevé, logique mal placée |
| Pas de facade (LLM doit connaître toutes les classes) | Moyenne | Contexte à charger plus grand, plus d'erreurs |
| Facade fine (delegation 1-ligne, logique dans la bonne classe) | Bonne | Point d'entrée unique + code maintenable + logique trouvable |

### La règle

Une facade est LLM-friendly si et seulement si ses méthodes sont des délégations d'une ligne.
Dès qu'une méthode de la facade contient de la logique propre, c'est un signal qu'elle a
grossi et doit être refactorisée.

---

## 11. Les méthodes courtes sont plus fiables que les méthodes longues

### Pourquoi

Un LLM lit une méthode entière pour la comprendre avant de la reproduire, la modifier ou la
compléter. Une méthode de 5 lignes est lue, comprise et reproduite correctement dans la
quasi-totalité des cas. Une méthode de 40 lignes avec des cas spéciaux, des conditions
imbriquées et des commentaires intercalés dépasse souvent la fenêtre d'attention effective
du modèle.

Le résultat concret : le LLM comprend le début et la fin de la méthode longue, mais peut
manquer une contrainte au milieu. Il génère quelque chose qui "ressemble" à la méthode mais
omet un cas limite. Ce type d'erreur est particulièrement difficile à détecter car le code
généré compile et peut même passer des tests superficiels.

### Le lien avec SRP et les classes cohésives

Les méthodes courtes sont un sous-produit naturel des classes cohésives. Quand chaque classe
a une seule responsabilité, ses méthodes traitent des cas simples et restent courtes. Les
méthodes longues sont souvent le symptôme d'une classe qui fait trop de choses.

Pour un LLM, ce n'est pas seulement une bonne pratique de code : c'est une condition pour
que la génération soit fiable.

### La règle pratique

Si une méthode dépasse 15-20 lignes, se demander si elle peut être découpée. Non pas pour
respecter une règle arbitraire, mais parce qu'une méthode longue est un signal que
plusieurs responsabilités ont été mélangées — et que le LLM risque de les confondre.

---

## 12. Chemins absolus dans la documentation de contexte

### Pourquoi

Un agent qui reçoit une référence à un fichier sans chemin doit le chercher par ses outils : glob, grep,
tentatives successives. Cette recherche consomme des tokens, prend du temps et peut aboutir
sur le mauvais fichier si le nom n'est pas unique.

Un chemin absolu (ou relatif depuis une racine explicite) élimine cette recherche. L'agent
ouvre directement le bon fichier. C'est l'équivalent, pour la documentation, de passer les
paramètres explicitement plutôt que de les laisser implicites dans l'état.

### S'applique à

Tout document de contexte (handoff, plan, spécification) qui référence des fichiers précis :
plans d'implémentation, points de vigilance, descriptions d'étapes. Exemples :

- Au lieu de "`Connecteur.java`, ligne 39" → "`src/main/java/app/connecteurs/Connecteur.java`, ligne 39"
- Au lieu de "le fichier cible de l'item" → "`src/main/java/noyau/ecran/BasePage.java`"

### La règle

Toute mention d'un fichier dans un document de contexte doit inclure son chemin complet
depuis la racine du projet. Sans chemin, c'est une information incomplète.

---

## 13. Les contradictions dans la documentation sont fatales pour un LLM

### Pourquoi

Un humain qui lit deux phrases contradictoires dans un document les réconcilie intuitivement :
il tient compte du contexte, de sa connaissance du projet, de l'ancienneté des informations.

Un LLM sans contexte projet ne peut pas faire ça. Face à une contradiction, il va :
- suivre la version qui apparaît en dernier (biais de position)
- halluciner une synthèse des deux qui satisfait les deux phrases sans en respecter aucune
- appliquer l'une des deux de façon aléatoire selon les passages

Aucune de ces issues n'est acceptable. Une contradiction dans la documentation n'est pas
un détail cosmétique — c'est un piège à hallucinations.

### Conséquence pratique

La revue de cohérence de la documentation est aussi importante que la revue de code
quand des LLMs interviennent. Types de contradictions à chasser :

- Deux sections décrivent le même comportement différemment
- Un document dit "à faire" et le code montre que c'est déjà fait
- Un document dit "méthode de A" et le code montre que c'est une méthode de B
- Un ancien nom et le nouveau nom coexistent sans que la migration soit explicitée

### La règle

Avant de donner un document à un LLM, le relire en cherchant activement les contradictions.
Un LLM ne saura pas ignorer ce qui est faux — il lira tout avec la même confiance.

---

## 14. Le bruit historique dans la documentation nuit plus qu'il n'aide

### Pourquoi

Un LLM lit tout ce qu'on lui donne. Il ne peut pas décider qu'un paragraphe est "obsolète"
ou "pour contexte seulement". Si l'information est là, elle influence la génération.

Une information historique — vraie à un état passé, maintenant dans le code — est doublement
dangereuse :
1. Elle consomme des tokens sans apporter de valeur opérationnelle
2. Elle peut contredire l'état actuel du code, créant une contradiction (voir section 13)

### Exemples typiques de bruit historique

- "La classe X s'appelait Y avant le refactoring" — l'ancien nom n'existe plus dans le code
- La liste détaillée de ce qui a été fait dans un item terminé — c'est dans git
- Les tables de renommage d'une migration achevée — c'est dans le code
- "Ce script est à créer" alors que le script existe déjà

### La règle

Si l'information est dans le code ou dans git, la supprimer du document. La documentation
de contexte doit être prospective, pas archivistique. La question à se poser pour chaque
ligne : "un agent qui reprend demain a-t-il besoin de lire ça pour agir ?"

Si la réponse est non, supprimer.

---

## 15. Éviter la surcharge de méthodes (overloading)

### Pourquoi

La surcharge de méthodes — plusieurs méthodes de même nom avec des signatures différentes —
est un mécanisme conçu pour l'IDE : l'autocomplétion propose les variantes, le développeur
choisit. Un LLM n'a pas ce mécanisme.

Face à `actionner(WebDriver driver, String valeur)` et `actionner(WebDriver driver)`, le LLM
doit lire les deux signatures pour choisir. Dans un contexte de génération, il peut se
tromper de variante, en inventer une troisième qui n'existe pas, ou fusionner les deux dans
une signature incorrecte.

### Cas limite : les surcharges légitimes

La recommandation ne s'applique pas quand les surcharges correspondent à des **types d'entrée
structurellement différents** qui ne peuvent pas être exprimés autrement. Exemple :

```java
// Legitime -- chaque surcharge accepte un type de locator fondamentalement different
cliquerQuandInteractable(WebDriver driver, WebElement parent, By child, int secondes)
cliquerQuandInteractable(WebDriver driver, By locator, int secondes)
cliquerQuandInteractable(WebDriver driver, String xpath, int secondes)
```

Les nommer distinctement donnerait `cliquerQuandInteractableAvecWebElementEtBy(...)` — moins
lisible que la surcharge. Dans ce cas, chaque variante doit être documentée avec un exemple
Javadoc expliquant quand l'utiliser. Le LLM choisit alors depuis la Javadoc, pas depuis
l'autocomplétion.

La règle reste : si deux surcharges ont des **contrats sémantiques différents** plutôt que des
types d'entrée différents, les nommer distinctement.

### Conséquence pratique

Des noms distincts portent le contrat dans le nom lui-même :

```java
// A eviter -- meme nom, contrats differents
void actionner(WebDriver driver)
void actionner(WebDriver driver, String valeur)

// Preferer -- noms distincts, contrats explicites dans le nom
void cliquer(WebDriver driver)
void actionnerAvecValeur(WebDriver driver, String valeur)
```

La longueur supplémentaire est négligeable pour un LLM. Le gain en clarté est significatif :
le LLM peut choisir la bonne méthode depuis son nom seul, sans lire les signatures.

---

## 16. Éviter les paramètres booléens

### Pourquoi

Un appel comme `charger(driver, true, false)` est illisible sans IDE. Le LLM doit aller
lire la déclaration de la méthode pour savoir ce que signifient `true` et `false`. Dans un
contexte de génération, il les invente ou les intervertit.

Ce principe est un cas particulier du §9 (constantes nommées) : un paramètre booléen est
une valeur magique (`true`/`false`) sans sémantique propre.

### Conséquences pratiques

**Enum nommé** quand la variante est un choix parmi plusieurs états :

```java
// A eviter
void charger(WebDriver driver, boolean rechargerSiDejaPresent)

// Preferer
enum ModeChargement { RECHARGER, CONSERVER }
void charger(WebDriver driver, ModeChargement mode)

// Appel lisible sans lire la signature
charger(driver, ModeChargement.RECHARGER)
```

**Méthodes distinctes** quand les variantes sont peu nombreuses et les noms naturels :

```java
void charger(WebDriver driver)
void recharger(WebDriver driver)
```

Dans les deux cas, le LLM peut choisir sans lire la signature. La sémantique est dans le nom.

---

## 17. La structure des packages est un index de navigation

### Pourquoi

Un LLM cherche une classe en inférant son package depuis son nom. Si le package est bien
nommé, la recherche se réduit à un répertoire. Un package fourre-tout (`outils`, `utils`,
`helpers`) force une recherche exhaustive dans l'ensemble du projet.

Ce principe est la même logique que §1 (noms auto-décrivants) appliquée à la granularité
supérieure. Un nom de package explicite est de la documentation gratuite que le LLM exploite
sans l'avoir lue.

### Exemple

```
noyau.ecran.champ     → le LLM sait que les classes de champ sont ici
noyau.selenium        → utilitaires Selenium
noyau.exceptions      → exceptions metier
```

Versus :

```
noyau.outils          → que contient "outils" ? Le LLM doit chercher.
noyau.utils           → idem
```

### La règle

Un package doit pouvoir être décrit par une responsabilité en une phrase courte. S'il ne
peut pas l'être, c'est un fourre-tout — le signal pour éclater.

Les noms `outils`, `utils`, `helpers`, `commun` ne sont pas interdits par principe, mais
ils doivent alerter : dès qu'un package ne peut plus être décrit en une phrase, il a grandi
au-delà de sa cohérence.

---

## 18. Organiser le code par intentions de navigation d'un agent froid

### Pourquoi

Un LLM qui reprend un projet à froid ne commence pas par une compréhension globale du
code. Il cherche un point d'entrée selon la tâche à accomplir :

- écrire un test ;
- comprendre une vue JSON ;
- corriger une interaction navigateur ;
- modifier le runner ;
- modifier le rapport ;
- comprendre le chargement des données de test ;
- toucher à la plomberie d'un framework sous-jacent comme TestNG.

Une organisation orientée uniquement par technologie (`selenium`, `json`, `testng`) ou
par historique des classes oblige le LLM à reconstruire la carte mentale du projet avant
d'agir. Cette phase de découverte consomme du contexte et augmente le risque qu'il modifie
le mauvais endroit.

L'organisation LLM-friendly ne part donc pas d'abord des classes existantes. Elle part des
intentions de navigation d'un agent froid. Une classe est placée là où un agent ira
naturellement la chercher pour accomplir une tâche. Le package devient une carte d'action,
pas seulement un rangement de fichiers.

### Le rôle mental prime sur la technologie

Une classe ne doit pas être placée uniquement parce qu'elle utilise une technologie.

Exemple : une classe qui manipule Selenium mais expose une opération de tableau métier
n'appartient pas forcément au package `selenium`. Si elle connaît les vues ou les tableaux,
elle appartient au domaine `vue.tableau`. Le package `selenium` doit rester réservé aux
primitives bas niveau Selenium.

Cette règle réduit les choix futurs :

- un agent qui corrige un clic WebDriver va dans `navigateur.selenium` ;
- un agent qui corrige la recherche dans une liste va dans `vue.tableau` ;
- un agent qui modifie l'écriture des tests va dans `api.test` ;
- un agent qui modifie un listener TestNG interne va dans `execution.testng`.

### Séparer API publique et mécanique interne

Pour un LLM, mélanger dans un même package les classes importées par les projets clients
et la plomberie interne est dangereux. L'agent peut lire ou modifier une classe interne
en croyant qu'elle fait partie de l'API.

Le pattern recommandé est :

```text
api/
  test/
  vue/

execution/
  testng/

vue/
  fluent/
  json/
  champ/
  tableau/
```

`api` contient ce qu'un projet client peut importer directement. Les autres packages sont
internes au framework, sauf exception explicitement documentée.

Cette séparation est plus déterministe qu'un package unique `test` contenant à la fois
`TestElementaire`, `Verifications`, `RetryAnalyzer` et `RetryTransformer`. Un agent qui
veut écrire un test ne doit pas voir la plomberie de retry comme une option plausible.

### Règles fermées de dépendance

Une organisation de packages n'est LLM-friendly que si ses frontières sont fermées.
Sinon, un agent peut interpréter différemment le placement d'une classe à chaque reprise.

Les règles doivent être écrites sous forme vérifiable :

```text
api peut dépendre des packages internes.
Les packages internes ne dépendent pas de api, sauf décision explicite.

vue peut dépendre de navigateur.selenium.
navigateur ne dépend jamais de vue.

api.test ne contient pas de classes nommées Retry*, Listener* ou Transformer*.
execution.testng contient la plomberie TestNG interne.

util est fermé : aucune nouvelle classe sans décision documentée.
```

Ces règles sont préférables à des formulations subjectives comme "mettre la classe dans le
package le plus logique". Pour un LLM probabiliste, une règle stricte et vérifiable produit
moins de divergence qu'une règle élégante mais interprétable.

### Documenter chaque package localement

Chaque package important doit contenir un `package-info.java` qui donne :

1. la responsabilité du package en une phrase ;
2. ce qui a le droit d'y entrer ;
3. ce qui est explicitement interdit ;
4. les packages voisins à utiliser en cas de confusion.

Exemple :

```java
/**
 * Primitives bas niveau autour du navigateur et de Selenium WebDriver.
 *
 * <p>Ce package ne contient pas de logique de vue, de tableau, de test ou de rapport.
 * Toute classe qui dépend de {@code vue} doit aller dans le domaine {@code vue}.
 */
package fr.natsystem.natbot.web.navigateur.selenium;
```

Cette documentation locale évite qu'un agent doive retrouver une règle globale dans un
document séparé pendant qu'il modifie un fichier précis.

### La règle

Organiser le code par intentions de navigation d'un agent froid, pas par historique et pas
uniquement par technologie.

Chaque package doit répondre à une question d'action :

- "où écrire ou comprendre l'API client ?"
- "où modifier le modèle de vue ?"
- "où modifier le navigateur bas niveau ?"
- "où modifier le runner ?"
- "où modifier le rapport ?"
- "où modifier les données de test ?"

Si un package ne répond pas clairement à une question d'action, il est trop vague ou mal
positionné.

---

## 19. Le document d'entrée unique

### Pourquoi

Les sections §12, §13, §14 et §18 traitent de la qualité interne d'un document de contexte
et de l'organisation du code.
Il manque un principe sur l'**architecture documentaire** elle-même.

Un LLM qui découvre un projet sans document d'entrée doit en déduire la structure par
tâtonnement : glob, grep, lecture de fichiers successifs. Cette découverte consomme des
tokens, introduit des lacunes, et peut aboutir sur une compréhension partielle ou incorrecte
de l'architecture.

Un document d'entrée unique résout ce problème. Il fournit d'emblée au LLM ce qu'un
développeur met des semaines à acquérir : la carte du projet.

### Ce qu'il doit contenir

Le document d'entrée n'est pas un README utilisateur. C'est un document technique pour
un agent qui va modifier le code :

- **Architecture en couches** : quelles classes, quelles responsabilités, quelles dépendances
- **Flux d'exécution** : comment une action se propage du point d'entrée jusqu'à l'effet
- **Patterns fondamentaux** : les conventions qui s'appliquent partout dans le code
- **Points d'attention** : les comportements contre-intuitifs ou non-déductibles du code seul
- **Chemins absolus** vers les fichiers clés (voir §12)

### Ce qu'il ne doit pas contenir

Voir §14 (fraîcheur) : pas d'historique, pas de listes de ce qui a été fait, pas de
décisions passées déjà intégrées dans le code. Un agent qui reprend le projet le lendemain
ne doit lire que ce qui lui est utile pour agir maintenant.

### La règle

Tout projet sur lequel un LLM intervient régulièrement doit avoir un document d'entrée
unique, tenu à jour, référencé en première position dans le README. Sa fraîcheur est aussi
critique que la fraîcheur du code. Un document d'entrée obsolète est aussi dangereux qu'une
contradiction (voir §13) : il oriente le LLM avec confiance dans la mauvaise direction.

---

## 20. Les Javadoc obsolètes ou en double sont pires que l'absence de Javadoc

### Pourquoi

Une Javadoc absente pousse le LLM à improviser depuis le nom de la méthode.
C'est risqué, mais le LLM sait qu'il improvise.

Une Javadoc qui dit le contraire de ce que fait le code est pire : le LLM
la lit avec confiance et génère du code structurellement incorrect. C'est
un cas spécial de §13 (contradictions), mais au niveau du code lui-même.

Exemple :

```java
/**
 * Retourne null si aucune ligne ne correspond.  ← ancienne Javadoc, maintenant fausse
 */
/**
 * Lève LigneIntrouvableException si aucune ligne ne correspond.  ← nouvelle Javadoc
 */
public Ligne chercherUneLigne(...) { ... }
```

Un LLM qui lit les deux blocs génère un `if (ligne == null)` -- code mort qui compilera
et masquera que le contrat a changé.

### Les deux formes dangereuses

**Javadoc en double** : deux blocs `/** */` consécutifs au-dessus d'une même méthode --
résidu d'une mise à jour partielle. Le LLM lit les deux et les combine, souvent de façon
incorrecte.

**Javadoc stale** : un seul bloc, mais dont le contenu décrit un comportement passé
(retour null → maintenant exception, paramètre supprimé → toujours décrit, etc.).

### La règle

Quand le comportement d'une méthode change : **supprimer l'ancienne Javadoc entièrement**
avant d'écrire la nouvelle. Ne jamais laisser deux blocs `/** */` au-dessus d'une même méthode.

La cohérence Javadoc/code est aussi importante que la cohérence entre documents (§13).
Un LLM ne distingue pas "commentaire obsolète" de "vérité actuelle" -- il lit les deux
avec la même confiance.

---

## Récapitulatif : les principes LLM-friendly

| Principe | Bonne pratique | A eviter |
|---|---|---|
| Variance | Conventions fermées, binaires, vérifiables par grep ou compilateur — l'absolutisme est une fonctionnalité | Conventions avec jugement ; règles avec exceptions ; formulations subjectives |
| Nommage | Noms longs et explicites | Abreviations, noms generiques |
| Taille des classes | Classes courtes et cohesives | Classes monolithes |
| API | Typee et consistante | Flat et surchargee |
| Documentation code | Javadoc avec exemple self-contained ; contraintes non-evidentes en prose ; aucun @param | Javadoc absente, repetant le nom, ou avec exemple incomplet ; @param qui reformule la signature |
| Erreurs | Messages explicites (attendu/constate) ; Optional<T> si absence legitime, exception typee si absence = erreur | Catch silencieux, messages vagues, retour null implicite |
| Encodage | ASCII dans les symboles du programme et les messages techniques ; accents dans la prose incorporée | Accents dans les identifiants ou messages techniques ; ASCII dans la documentation |
| Parametres | Explicites | Implicites via etat |
| Abstractions | Justifiees par un besoin reel | Speculatives |
| Constantes | Nommees semantiquement | Valeurs magiques |
| Facade | Fine (delegation 1-ligne) | Grasse (logique incluse) ou absente |
| Methodes | Courtes (moins de 15-20 lignes) | Longues avec cas imbriques |
| Chemins | Absolus dans tout document de contexte | Noms de fichier sans chemin |
| Coherence doc | Zero contradiction entre sections | Informations contradictoires |
| Fraicheur doc | Prospective, sans historique obsolete | Bruit historique, etat passe |
| Surcharge | Noms distincts par contrat ; surcharges acceptables si types d'entree structurellement differents + Javadoc | Overloading avec contrats semantiques differents sous le meme nom |
| Javadoc code | Un seul bloc, a jour avec le comportement reel | Double Javadoc (ancienne + nouvelle), Javadoc stale (decrit l'ancien comportement) |
| Booleens | Enum nomme ou methodes distinctes | Parametres booleens positionnels |
| Packages | Nommes par domaine, une responsabilite par package | Fourre-tout (utils, outils, helpers) |
| Organisation du code | Packages alignes sur les intentions de navigation d'un agent froid ; API publique separee de l'interne ; regles de dependance fermees | Organisation par historique ou technologie seule ; API et plomberie melangees ; frontieres interpretables |
| Document d'entree | Un seul document de reference, tenu a jour | Decouverte par tâtonnement |
