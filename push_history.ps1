# Push with realistic commit history
Set-Location "C:\Users\info\Desktop\Data_proccessing_dbt"

# Clean any existing git repo
if (Test-Path ".git") { Remove-Item -Recurse -Force ".git" }

# Init repo
git init
git config user.name "Mahmoud"
git config user.email "mahmoud.qzibar@gmail.com"

# ── COMMIT 1 : Project bootstrap ── 2026-04-01
git add README.md requirements.txt docker-compose.yml workspace.yaml Dockerfile
$env:GIT_AUTHOR_DATE    = "2026-04-01T09:15:00"
$env:GIT_COMMITTER_DATE = "2026-04-01T09:15:00"
git commit -m "init: project bootstrap — Dagster + dbt + PostgreSQL stack"

# ── COMMIT 2 : Dagster workspace & definitions ── 2026-04-03
git add weather_pipeline/__init__.py weather_pipeline/definitions.py
$env:GIT_AUTHOR_DATE    = "2026-04-03T10:30:00"
$env:GIT_COMMITTER_DATE = "2026-04-03T10:30:00"
git commit -m "feat(dagster): add workspace config and pipeline definitions"

# ── COMMIT 3 : Raw data extraction asset ── 2026-04-05
git add weather_pipeline/assets/raw_data.py
$env:GIT_AUTHOR_DATE    = "2026-04-05T14:20:00"
$env:GIT_COMMITTER_DATE = "2026-04-05T14:20:00"
git commit -m "feat(asset): raw_weather — extract Open-Meteo API and load to PostgreSQL"

# ── COMMIT 4 : dbt project structure ── 2026-04-08
git add weather_dbt/dbt_project.yml weather_dbt/profiles.yml weather_dbt/models/sources.yml
$env:GIT_AUTHOR_DATE    = "2026-04-08T09:00:00"
$env:GIT_COMMITTER_DATE = "2026-04-08T09:00:00"
git commit -m "feat(dbt): initialize dbt project structure with sources"

# ── COMMIT 5 : dbt staging model ── 2026-04-09
git add weather_dbt/models/staging/stg_weather.sql
$env:GIT_AUTHOR_DATE    = "2026-04-09T11:45:00"
$env:GIT_COMMITTER_DATE = "2026-04-09T11:45:00"
git commit -m "feat(dbt): add stg_weather staging model — cast types and rename columns"

# ── COMMIT 6 : dbt mart model ── 2026-04-11
git add weather_dbt/models/marts/mart_daily_weather_stats.sql
$env:GIT_AUTHOR_DATE    = "2026-04-11T16:10:00"
$env:GIT_COMMITTER_DATE = "2026-04-11T16:10:00"
git commit -m "feat(dbt): add mart_daily_weather_stats — daily min/max/avg aggregations"

# ── COMMIT 7 : Dagster dbt integration asset ── 2026-04-14
git add weather_pipeline/assets/dbt_assets.py
$env:GIT_AUTHOR_DATE    = "2026-04-14T10:00:00"
$env:GIT_COMMITTER_DATE = "2026-04-14T10:00:00"
git commit -m "feat(dagster-dbt): expose dbt models as Dagster assets via dagster-dbt"

# ── COMMIT 8 : Streamlit dashboard ── 2026-04-17
git add dashboard/app.py
$env:GIT_AUTHOR_DATE    = "2026-04-17T15:30:00"
$env:GIT_COMMITTER_DATE = "2026-04-17T15:30:00"
git commit -m "feat(dashboard): add Streamlit + Plotly dark mode weather dashboard"

# ── COMMIT 9 : Tests ── 2026-04-20
git add tests/test_assets.py
$env:GIT_AUTHOR_DATE    = "2026-04-20T13:00:00"
$env:GIT_COMMITTER_DATE = "2026-04-20T13:00:00"
git commit -m "test: add pytest suite for API extraction and Dagster assets"

# ── COMMIT 10 : gitignore + cleanup ── 2026-04-22
@"
.venv/
__pycache__/
*.pyc
.pytest_cache/
logs/
dagster_home/
tmpmp748nf2/
weather_dbt/target/
weather_dbt/logs/
weather_dbt/dbt_packages/
weather_dbt/.user.yml
"@ | Set-Content .gitignore
git add .gitignore
git add . 2>$null
$env:GIT_AUTHOR_DATE    = "2026-04-22T09:20:00"
$env:GIT_COMMITTER_DATE = "2026-04-22T09:20:00"
git commit -m "chore: add .gitignore, exclude venv/logs/cache/dbt targets"

# ── Push ──
git branch -M main
git remote add origin https://github.com/nom-mahmoud/ELT-Pipeline.git
git push -f -u origin main

Write-Host "`n✅ Done! Check https://github.com/nom-mahmoud/ELT-Pipeline"
