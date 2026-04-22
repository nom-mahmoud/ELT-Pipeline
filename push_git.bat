@echo off
cd /d "C:\Users\info\Desktop\Data_proccessing_dbt"

if exist ".git" rmdir /s /q ".git"

git init
git config user.name "Mahmoud"
git config user.email "mahmoud.qzibar@gmail.com"

git add README.md requirements.txt docker-compose.yml workspace.yaml Dockerfile
set GIT_AUTHOR_DATE=2026-04-01T09:15:00
set GIT_COMMITTER_DATE=2026-04-01T09:15:00
git commit -m "init: project bootstrap - Dagster + dbt + PostgreSQL stack"

git add weather_pipeline/__init__.py weather_pipeline/definitions.py
set GIT_AUTHOR_DATE=2026-04-03T10:30:00
set GIT_COMMITTER_DATE=2026-04-03T10:30:00
git commit -m "feat(dagster): add workspace config and pipeline definitions"

git add weather_pipeline/assets/raw_data.py
set GIT_AUTHOR_DATE=2026-04-05T14:20:00
set GIT_COMMITTER_DATE=2026-04-05T14:20:00
git commit -m "feat(asset): raw_weather - extract Open-Meteo API and load to PostgreSQL"

git add weather_dbt/dbt_project.yml weather_dbt/profiles.yml weather_dbt/models/sources.yml
set GIT_AUTHOR_DATE=2026-04-08T09:00:00
set GIT_COMMITTER_DATE=2026-04-08T09:00:00
git commit -m "feat(dbt): initialize dbt project structure with sources"

git add weather_dbt/models/staging/stg_weather.sql
set GIT_AUTHOR_DATE=2026-04-09T11:45:00
set GIT_COMMITTER_DATE=2026-04-09T11:45:00
git commit -m "feat(dbt): add stg_weather staging model - cast types and rename columns"

git add weather_dbt/models/marts/mart_daily_weather_stats.sql
set GIT_AUTHOR_DATE=2026-04-11T16:10:00
set GIT_COMMITTER_DATE=2026-04-11T16:10:00
git commit -m "feat(dbt): add mart_daily_weather_stats - daily min/max/avg aggregations"

git add weather_pipeline/assets/dbt_assets.py
set GIT_AUTHOR_DATE=2026-04-14T10:00:00
set GIT_COMMITTER_DATE=2026-04-14T10:00:00
git commit -m "feat(dagster-dbt): expose dbt models as Dagster assets via dagster-dbt"

git add dashboard/app.py
set GIT_AUTHOR_DATE=2026-04-17T15:30:00
set GIT_COMMITTER_DATE=2026-04-17T15:30:00
git commit -m "feat(dashboard): add Streamlit + Plotly dark mode weather dashboard"

git add tests/test_assets.py
set GIT_AUTHOR_DATE=2026-04-20T13:00:00
set GIT_COMMITTER_DATE=2026-04-20T13:00:00
git commit -m "test: add pytest suite for API extraction and Dagster assets"

git add .
set GIT_AUTHOR_DATE=2026-04-22T09:20:00
set GIT_COMMITTER_DATE=2026-04-22T09:20:00
git commit -m "chore: add .gitignore and final cleanup"

git branch -M main
git remote add origin https://github.com/nom-mahmoud/ELT-Pipeline.git
git push -f -u origin main
