# Générateur de recettes

Site web qui propose des recettes à partir des ingrédients disponibles et de contraintes (allergies, régime).

Projet réalisé dans le cadre du Master Numérique, Enjeux et Technologies.

## Problème
Quand on ouvre son frigo, on sait rarement quoi cuisiner avec ce qu'on a, surtout avec des allergies ou un régime. Les sites de recettes classiques partent du plat, pas des ingrédients disponibles.

## Automatisation
Le site enchaîne sans intervention manuelle : lecture des ingrédients, traduction, interrogation de l'API, classement des recettes par nombre d'ingrédients correspondants, exclusion des allergènes et des régimes incompatibles, puis affichage de la fiche avec vidéo.

## Version 1 (livrée)
- Saisie d'ingrédients (français ou anglais).
- Filtres : allergies (gluten, lait, œufs, arachides, poisson / fruits de mer) et régime (végétarien, sans porc).
- Classement des recettes par nombre d'ingrédients trouvés.
- Fiche recette : ingrédients, préparation, vidéo YouTube intégrée si disponible.

## Feuille de route
| Version | Contenu |
|---|---|
| V2 | Contraintes de temps et de budget, avec un jeu de recettes en français enrichi (JSON) |
| V3 | Profil utilisateur et recommandations personnalisées (filtrage basé sur le contenu, profil stocké dans le navigateur) |
| V4 | Valeurs nutritionnelles du plat (Open Food Facts) |
| V5 | Scan de code-barres, planning de repas, liste de courses |

## Choix techniques
| Besoin | Solution |
|---|---|
| Hébergement | GitHub Pages (site statique) |
| Front | HTML, CSS, JavaScript |
| Recettes et vidéos | API TheMealDB (gratuite, sans clé) |

## Limites connues
- Les recettes de TheMealDB sont en anglais.
- L'API gratuite filtre un seul ingrédient à la fois : le classement est calculé côté navigateur.
- La détection des allergènes repose sur des mots-clés dans les ingrédients : elle est indicative et ne remplace pas la vérification des étiquettes.
- Le temps de préparation et le budget ne sont pas disponibles dans l'API.

## Lancer en local
Ouvrir `index.html` dans un navigateur.
