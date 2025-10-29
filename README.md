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

## Vue globale
![Global](images/vue_global.png)



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
