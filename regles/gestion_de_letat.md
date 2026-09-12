# Règles de gestion de l'état mutable

Ce document complète [conception.md](conception.md), notamment ses sections sur l’immuabilité,
les fonctions pures et l’état borné. Il détaille leur application aux composants avec état.

Ces règles s’appliquent à la conception de tout composant ou système dont l'état peut évoluer au cours de l'exécution.
Elles sont organisées par stratégie et formulées comme des règles binaires vérifiables.

## Réduire l'état mutable

- Préférer les valeurs immuables aux références mutables. Une donnée qui ne change pas ne peut pas être dans un état incohérent.
- Pousser les décisions et les transformations dans des fonctions pures. Une fonction pure produit toujours la même sortie pour les mêmes entrées, sans effet de bord.
- Séparer ce qui décide (functional core) de ce qui agit (imperative shell). Le core ne lit ni n'écrit d'état externe. L'imperative shell lit l'état du monde, appelle le core, écrit le résultat.

## Contenir et localiser l'état mutable

- L'état appartient à un seul composant. Personne d'autre ne lit ni n'écrit directement dedans.
- Un composant qui fait une seule chose possède un état cohérent et borné. Quand un composant gère plusieurs états sans lien, le découper.
- Ne pas traverser les graphes d'objets pour atteindre un état distant. Chaque composant parle à ses voisins directs (Loi de Déméter).

## Rendre les mutations explicites

- Une méthode qui lit ne modifie pas. Une méthode qui modifie ne retourne pas de valeur. Les deux ne se mélangent pas (Command Query Separation).
- Dire à un composant quoi faire plutôt que lire son état pour décider à sa place. La décision et la mutation restent au même endroit (Tell, Don't Ask).
- Énumérer les états possibles et définir les transitions explicitement. Un état invalide doit être structurellement impossible (State Machine).
- Enregistrer les mutations comme des événements immuables si le contexte le justifie (systèmes distribués, audit trail, replay). Ne pas appliquer Event Sourcing à un simple pipeline local — le surcoût de complexité n'est pas justifié.

## Rendre les dépendances à l'état visibles

- L'état externe est passé en paramètre, pas capturé implicitement. La signature d'une fonction dit ce dont elle a besoin.
- Les mutations circulent dans un seul sens, par un point d'entrée connu. Jamais par un effet de bord dispersé dans le code (flux de données unidirectionnel).
- Pas de variables globales mutables. Si un état doit être partagé, le rendre explicite et injecter sa référence.

## Coordonner les mutations

- Regrouper les mutations qui doivent rester cohérentes en unités atomiques. Soit tout réussit, soit rien n'est écrit (Unit of Work).
- Garantir les invariants de cohérence à travers plusieurs mutations simultanées ou concurrentes (transactions).
- Après une mutation, vérifier que les invariants du composant sont respectés avant de rendre la main.

## Exemples

### Command Query Separation (CQS)

```java
// Mauvais : lit et modifie en même temps
public Statut validerEtRetournerStatut() {
    this.statut = Statut.VALIDE;
    return this.statut;
}

// Bon : séparation lecture / mutation
public void valider() {
    this.statut = Statut.VALIDE;
}

public Statut obtenirStatut() {
    return this.statut;
}
```

```python
# Mauvais
def integrer_et_retourner_compte(self, ligne):
    self.lignes.append(ligne)
    return len(self.lignes)

# Bon
def integrer(self, ligne):
    self.lignes.append(ligne)

def compte(self):
    return len(self.lignes)
```

### Tell, Don't Ask

```java
// Mauvais : lire l'état pour décider à la place du composant
if (commande.getStatut() == Statut.EN_ATTENTE) {
    commande.setStatut(Statut.VALIDEE);
}

// Bon : dire au composant quoi faire
commande.valider();
```

### Functional Core / Imperative Shell

```python
# Core : pur, testable sans I/O
def groupes_manquants(ids_groupes: list[str], analyse: dict) -> list[str]:
    return [id for id in ids_groupes if not groupe_termine(id, analyse)]

# Shell : lit les fichiers, appelle le core, écrit le résultat
def continuer_analyse(application: str):
    groupes = lire_groupes(application)        # I/O
    analyse = lire_analyse(application)         # I/O
    manquants = groupes_manquants(groupes, analyse)  # core pur
    for groupe in manquants:
        traiter_groupe(application, groupe)     # I/O
```

### État invalide structurellement impossible

```java
// Mauvais : l'état invalide est possible à construire
public class Analyse {
    private String application;  // peut être null
    private List<Ligne> lignes;  // peut être null
}

// Bon : l'état invalide est impossible à construire
public class Analyse {
    private final String application;
    private final List<Ligne> lignes;

    public Analyse(String application, List<Ligne> lignes) {
        Objects.requireNonNull(application, "application obligatoire");
        Objects.requireNonNull(lignes, "lignes obligatoires");
        this.application = application;
        this.lignes = List.copyOf(lignes);
    }
}
```

## Tester les composants avec état

- Tester à travers l'interface publique, jamais en accédant directement aux champs internes.
- Utiliser des méthodes de fabrique pour construire les états initiaux des tests : l'état de départ est explicite et lisible.
- Vérifier le comportement observable (valeur retournée, exception levée, état lu via accesseur), pas l'état interne.
- Un test qui reflète les champs privés via reflection est un test fragile — il teste l'implémentation, pas le contrat.
- Tester les transitions d'état : état initial → mutation → état attendu.
- Tester les transitions invalides : une transition interdite doit lever une exception ou être refusée, pas silencieusement ignorée.

```java
// Mauvais : accès à l'état interne
@Test
void valider_met_statut_a_valide() {
    Commande commande = new Commande();
    commande.valider();
    assertEquals(Statut.VALIDE, commande.statut);  // champ privé exposé
}

// Bon : vérification par le contrat public
@Test
void valider_rend_la_commande_validee() {
    Commande commande = Commande.enAttente("CMD-001");
    commande.valider();
    assertTrue(commande.estValidee());
}

// Tester la transition invalide
@Test
void valider_une_commande_deja_validee_leve_une_exception() {
    Commande commande = Commande.enAttente("CMD-001");
    commande.valider();
    assertThrows(TransitionInvalideException.class, commande::valider);
}
```

## Relation entre les principes

Ces principes se combinent. Un bon design en applique plusieurs simultanément selon la nature de l'état à gérer :

- État local et transitoire : immutabilité + fonctions pures + CQS.
- État avec transitions métier : State Machine + Tell Don't Ask + encapsulation.
- État persisté partagé : injection de dépendances + Unit of Work + transactions.
- État distribué sur plusieurs composants : Functional Core / Imperative Shell + flux unidirectionnel.
