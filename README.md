# Journal alimentaire

Site web de suivi de l'alimentation inspiré de MyFitnessPal et Yazio : on note ce qu'on mange, le site calcule les calories et les macronutriments de la journée. Les recettes deviennent une fonction secondaire d'inspiration.

Projet réalisé dans le cadre du cours de programmation Web (Master Numérique, Enjeux et Technologies).

## Pages du projet
| Page | Contenu |
|---|---|
| `index.html` | Accueil avec liens vers les versions |
| `index0.html` | Version 1 : recettes par ingrédients, allergies, régime, vidéo |
| `index1.html` | Version 2 : favoris et recommandations personnalisées |
| `index2.html` | Version 3 : journal alimentaire (fonction principale) et idées de repas |
| `grist-widget.html` | Test d'une vue personnalisée Grist qui affiche les données d'un tableau |

## Problème
Suivre ce qu'on mange est fastidieux : il faut chercher les valeurs nutritionnelles de chaque aliment et faire les additions. Le site automatise la recherche des aliments, le calcul des calories et des macros, et la comparaison avec un objectif quotidien.

## Version 3 : fonctionnalités
- Journal par jour avec quatre repas (petit-déjeuner, déjeuner, dîner, collations).
- Recherche d'un aliment par nom ou par code-barres (Open Food Facts), quantité en grammes, calcul des calories et des macros.
- Tableau de bord : total du jour, objectif de calories, calories restantes, répartition protéines, glucides, lipides.
- Suivi de l'eau.
- Profil : objectif de calories modifiable. Données stockées dans le navigateur (localStorage).
- Onglet « Idées de repas » : recettes proposées à partir d'ingrédients (TheMealDB), avec vidéo, et ajout au journal avec calories saisies à la main.

## Feuille de route
| Version | Contenu |
|---|---|
| V1 | Recettes par ingrédients, allergies, régime, vidéo (livrée) |
| V2 | Favoris et recommandations personnalisées (livrée) |
| V3 | Journal alimentaire, calories et macros (livrée) |
| V4 | Scan de code-barres avec la caméra (ZXing-js ou Quagga2), historique et graphiques |
| V5 | Calcul des besoins à partir du profil, suivi du poids, recettes avec valeurs nutritionnelles |

## Choix techniques
| Besoin | Solution |
|---|---|
| Hébergement | GitHub Pages (site statique) |
| Front | HTML, CSS, JavaScript |
| Aliments et nutriments | API Open Food Facts |
| Idées de repas et vidéos | API TheMealDB |
| Données utilisateur | localStorage |
| Données tabulaires | Grist (vue personnalisée) |

## Limites connues
- Open Food Facts est centrée sur les produits emballés : les aliments bruts (oignon, carotte) sont moins bien couverts.
- Les valeurs de la base sont collaboratives et peuvent contenir des erreurs.
- Les recettes de TheMealDB sont en anglais et n'ont pas de valeurs nutritionnelles : les calories sont saisies à la main.
- Les données restent dans un seul navigateur, sans compte utilisateur.
- Le site donne des estimations indicatives et ne remplace pas un avis diététique.
