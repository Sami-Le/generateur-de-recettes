# Journal alimentaire

Site web de suivi de l'alimentation inspiré de MyFitnessPal et Yazio : on note ce qu'on mange, le site calcule les calories et les macronutriments de la journée. Les recettes sont une fonction secondaire d'inspiration, avec un accent sur les repas et collations riches en protéines.

Projet réalisé dans le cadre du cours de programmation Web (Master Numérique, Enjeux et Technologies).

## Pages du projet
| Page | Contenu |
|---|---|
| `index.html` | Accueil avec liens vers les versions |
| `index0.html` | Version 1 : recettes par ingrédients, allergies, régime, vidéo |
| `index1.html` | Version 2 : favoris et recommandations personnalisées |
| `index2.html` | Version 3 : journal alimentaire (fonction principale) et idées de repas |
| `index3.html` | Version 4 : recettes protéinées en français, nutrition calculée, mode Spoonacular |
| `recettes.json` | Données de la V4 : tableau d'ingrédients et recettes |
| `grist-widget.html` | Test d'une vue personnalisée Grist (le test demandé a été fait avec le Custom Widget Builder dans Grist) |

## Problème
Suivre ce qu'on mange est fastidieux : il faut chercher les valeurs nutritionnelles de chaque aliment et faire les additions. Le site automatise la recherche des aliments, le calcul des calories et des macros, et la comparaison avec un objectif quotidien.

## Version 4 : recettes protéinées
- 12 recettes en français : 4 repas, 4 collations sucrées, 4 collations salées.
- La nutrition par portion est calculée automatiquement dans le navigateur à partir des ingrédients en grammes et d'un tableau d'ingrédients (calories, protéines, glucides, lipides pour 100 g).
- Filtres : type de recette, protéines minimales par portion, recherche par nom ou ingrédient. Les résultats sont triés par protéines décroissantes.
- Bouton pour ajouter une portion au journal alimentaire de la V3, avec les vraies valeurs.
- Mode Spoonacular (démonstration) : recherche avec filtre minimal de protéines, sur une base plus large en anglais. La clé d'API est saisie par l'utilisateur et reste dans son navigateur. Le plan gratuit est limité à 50 points par jour.
- Pour ajouter une recette : éditer `recettes.json` (ingrédients par id, quantités en grammes, étapes).

## Feuille de route
| Version | Contenu |
|---|---|
| V1 | Recettes par ingrédients, allergies, régime, vidéo (livrée) |
| V2 | Favoris et recommandations personnalisées (livrée) |
| V3 | Journal alimentaire, calories et macros (livrée) |
| V4 | Recettes protéinées en français, nutrition calculée, Spoonacular (livrée) |
| V5 | Scan de code-barres avec la caméra, historique et graphiques, calcul des besoins, plus de recettes |
| Piste | Veille automatique de recettes populaires (tâche planifiée qui met à jour un fichier JSON après relecture humaine) |

## Choix techniques
| Besoin | Solution |
|---|---|
| Hébergement | GitHub Pages (site statique) |
| Front | HTML, CSS, JavaScript |
| Aliments emballés | API Open Food Facts |
| Recettes françaises | Fichier `recettes.json` |
| Recettes en anglais | API TheMealDB (V1 à V3), API Spoonacular (V4) |
| Données utilisateur | localStorage |
| Données tabulaires | Grist (vue personnalisée) |

## Limites connues
- Les valeurs du tableau d'ingrédients de `recettes.json` sont approximatives et à vérifier avec la table Ciqual de l'ANSES.
- Seulement 12 recettes françaises pour l'instant.
- Spoonacular : résultats en anglais, clé personnelle nécessaire, quota gratuit limité.
- Open Food Facts est centrée sur les produits emballés, ses valeurs sont collaboratives et peuvent contenir des erreurs.
- Les recettes tendance des réseaux sociaux ne peuvent pas être récupérées directement (API de recherche TikTok réservée aux chercheurs, API Instagram destinée aux comptes professionnels).
- Les données restent dans un seul navigateur, sans compte utilisateur.
- Estimations indicatives, qui ne remplacent pas un avis diététique.
