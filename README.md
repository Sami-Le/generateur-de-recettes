# Générateur de recettes

Site web qui propose des recettes à partir des ingrédients disponibles et de contraintes (allergies, régime).

Projet réalisé dans le cadre du cours de programmation Web (Master Numérique, Enjeux et Technologies).

## Pages du projet
| Page | Contenu |
|---|---|
| `index.html` | Accueil avec liens vers les versions |
| `index0.html` | Version 1 : recettes par ingrédients, allergies, régime, vidéo |
| `index1.html` | Version 2 : ajoute les favoris et les recommandations personnalisées |
| `grist-widget.html` | Test d'une vue personnalisée Grist qui affiche les données d'un tableau |

## Problème
Quand on ouvre son frigo, on sait rarement quoi cuisiner avec ce qu'on a, surtout avec des allergies ou un régime. Les sites de recettes classiques partent du plat, pas des ingrédients disponibles.

## Automatisation
Le site enchaîne sans intervention manuelle : lecture des ingrédients, traduction, interrogation de l'API, classement des recettes, exclusion des allergènes et des régimes incompatibles, puis affichage de la fiche avec vidéo.

## Version 2 : personnalisation
Chaque fois que l'utilisateur aime une recette, son profil (catégories et cuisines préférées) est enregistré dans le navigateur (localStorage). Le score d'une recette combine le nombre d'ingrédients trouvés (poids 10) et l'affinité avec le profil. C'est un filtrage basé sur le contenu simplifié. Les recettes recommandées reçoivent le badge « Pour toi ».

## Feuille de route
| Version | Contenu |
|---|---|
| V1 | Recettes par ingrédients, allergies, régime, vidéo (livrée) |
| V2 | Favoris et recommandations personnalisées (livrée) |
| V3 | Temps et budget, avec un jeu de recettes françaises en JSON ou Grist |
| V4 | Valeurs nutritionnelles du plat (Open Food Facts) |
| V5 | Scan de code-barres, planning de repas, liste de courses |

## Choix techniques
| Besoin | Solution |
|---|---|
| Hébergement | GitHub Pages (site statique) |
| Front | HTML, CSS, JavaScript |
| Recettes et vidéos | API TheMealDB (gratuite, sans clé) |
| Profil | localStorage |
| Données tabulaires | Grist (vue personnalisée) |

## Limites connues
- Les recettes de TheMealDB sont en anglais.
- L'API gratuite filtre un seul ingrédient à la fois : le classement est calculé côté navigateur.
- La détection des allergènes repose sur des mots-clés : elle est indicative.
- Le profil est local à un navigateur, sans compte utilisateur.
- Le temps de préparation et le budget ne sont pas disponibles dans l'API.
