# Projet de Pipeline de Données : Météo avec Dagster, dbt et PostgreSQL

## 🎯 Objectif du projet
Ce projet implémente une pipeline de données de bout en bout (ELT) pour récupérer, transformer et visualiser des données météorologiques issues de l'API publique Open-Meteo.

## 🛠️ Stack Technologique
- **Orchestration** : Dagster
- **Base de données** : PostgreSQL (Serveur robuste de base de données relationnelle)
- **Transformations (T)** : dbt (Data Build Tool) couplé à PostgreSQL
- **Visualisation** : Streamlit avec des graphiques Plotly (Design Premium Dark Mode)
- **Tests** : pytest
- **Conteneurisation** : Docker & Docker Compose

## 🏗️ Architecture
1. **Extraction** : Un asset Dagster récupère l'historique des températures horaires depuis l'API Open-Meteo.
2. **Chargement (Load)** : Ces données brutes sont insérées dans une table `raw_weather` dans PostgreSQL.
3. **Transformation** : Des modèles dbt (`stg_weather`, `mart_daily_weather_stats`) prennent en charge le nettoyage et l'agrégation des données. L'exécution de dbt est orchestrée de manière unifiée au sein du job Dagster grâce à `dagster-dbt`.
4. **Visualisation** : L'application Streamlit lit le data mart final pour proposer un Dashboard dynamique d'analyse des tendances.

## 🚀 Lancement Rapide (Local)

*Prérequis: Un serveur PostgreSQL doit être accessible (en local ou via docker).*

1. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

2. **Démarrer Dagster (Orchestrateur UI)** :
```bash
dagster dev
```
Rendez-vous sur http://localhost:3000, allez dans l'onglet "Assets" et cliquez sur **Materialize All** pour lancer la pipeline complète.

3. **Démarrer Streamlit (Dashboard UI)** :
Ouvrez un autre terminal :
```bash
streamlit run dashboard/app.py
```
Accédez au tableau de bord sur http://localhost:8501.

## 🐳 Lancement via Docker (Bonus)
Pour déployer le projet entièrement avec Docker :
```bash
docker-compose up --build
```
- Dagster UI : http://localhost:3000
- Dashboard Streamlit : http://localhost:8501

*(Note: via l'UI Dagster Dockerisée, matérialisez les assets pour voir les données apparaitre dans le dashboard streamllit)*

## ✅ Tests
Pour lancer la suite de tests (vérification de l'extraction API et intégration des assets) :
```bash
pytest tests/
```
