# Energy-Tracking 
J'ai commençé à m'intéresser à mes consommation de gaz et d'électricité lorsque mon fournisseur m'indiquait: "vous consommez plus que les foyers de similaire..." 😒
sans trop savoir comment mon fournisseur avait plus établir ses critères de similarité, j'ai dévellopé cet application pour suivre, traiter et visualiser mes données de consommation de gaz et électricité.
Les données sont récupérées quotidiennement via une API que j'ai développé dans un autre projet.
![Architecture](images/architecture_application.png)

L'application permet:
- De visualiser les consommations à la maille annuelle, mensuelle, journalière et horaire (uniquement pour l'électricité)
- Comparer les consommations sur des périodes identiques
- Comparer les consommations par rapport à un modèle basé sur la rigueur climatique et le taux d'occupation du logement
- d'injecter les données journalière de consommation gaz (il n'y a pas d'accès à l'API GRFD pour les particuliers)
- D'afficher des informations sur les données (distribution, données manquantes, périodes couvertes)

## Aperçu de l'application

### Menu *global*
La vue globale affiche les consommations annuelles ansi que les variations de consommations par rapport à l'année précédente, de date à date (Ex: si la date de consultation du rapport est le 11/10/2025, on compare avec les consommations cumulées du 01/01/2024 au 11/10/2024)

<p align="center">
  <img src="images/vue_global.png" alt="global1" width="65%"/>
</p>

L'onglet *Historique mensuel* affiche les consommations mensuelles ainsi que les DJU
<p align="center">
  <img src="images/vue_global_conso_mensuelles.png" alt="global2" width="65%"/>
</p>


### Menu *Electricité*
Visualisation des consommations horaires, journalières et mensuelles

#### *consommations horaires*
Outre l'historique de consommation horaire, l'application permet de visusaliser les profils horaires moyen pour les différents jours de la semaine, avec possibilité de sélectionner une période d'étude. Cela permet d'identifier les pics de consommations
<p align="center">
  <img src="images/elec_horaire_1.png" alt="global3" width="45%"/>
  <img src="images/elec_horaire_heatmap_profils.png" alt="global2" width="45%"/>
</p>


#### *consommations mensuelles*

Le graphe de gauche permet de visualiser les consommations mensuelles et de les comparer avec un modèle. Ce est modèle est une régression linéaire apprises sur la période 2023 à 2024 et fonction de 2 facteurs: les DJU et le taux d'occupation du logement. L'intervalle de confiance (à 95%) du modèle est représenté par les barres verticales. Celui reste assez élevé compte-tenue de la difficulté à modéliser la consommation d'un logement individuel, par rapport un groupe de logements pour lesquels les effets stochastiques liés au comportement tendent à s'estomper (et ceci plus il y'a de logements).
Le graphe de droite propose les consommations mensuelles groupées par année.

<p align="center">
  <img src="images/elec_mois_conso_modele.png" alt="global4" width="45%"/>
  <img src="images/elec_mois_conso_groupee_mois.png" alt="global5" width="45%"/>
</p>

## ⚙️ Technologie utilisées

- RDS AWS pour le stockage des données dans une base PostgreSQL
- S3 AWS pour le stockage des données GRDF
- EC2 AWS pour l'hébergement de l'API sur un serveur virtuel
- Python pour le code avec:
  - FastAPI pour le framework de l'API
  - apscheduler pour les appels quotidients des API météo et Linky
  - sqlalchemy pour l'insertion et la gestion des données vers PostgreSQL
- Docker pour le déploiement de l'API sur EC2

## 🗂️ Installation


- Construire l'image docker et lancer le conteneur
  -  docker compose up -d --build
