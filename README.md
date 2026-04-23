# Weather ELT Pipeline — Dagster, dbt & PostgreSQL

A production-ready ELT pipeline that ingests historical weather data from the Open-Meteo API, loads it into PostgreSQL, transforms it with dbt, and serves it through an interactive Streamlit dashboard.

## Stack

| Layer | Technology |
|---|---|
| Orchestration | Dagster + dagster-dbt |
| Storage | PostgreSQL |
| Transformation | dbt (data build tool) |
| Visualization | Streamlit + Plotly |
| Testing | pytest |
| Containerization | Docker & Docker Compose |

## Architecture

```
Open-Meteo API
      │
      ▼
Dagster Asset (raw_weather)
      │  Extract & Load
      ▼
PostgreSQL — raw_weather table
      │
      ▼
dbt (dagster-dbt)
  ├── stg_weather         (staging: type casting, renaming)
  └── mart_daily_weather_stats  (daily min/max/avg aggregations)
      │
      ▼
Streamlit Dashboard
```

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL running locally or via Docker

### Run locally

```bash
pip install -r requirements.txt
```

Start the orchestrator:
```bash
dagster dev
```

Open the Dagster UI at http://localhost:3000, navigate to **Assets** and click **Materialize All** to trigger the full pipeline.

Start the dashboard in a second terminal:
```bash
streamlit run dashboard/app.py
```

Dashboard available at http://localhost:8501.

### Run with Docker

```bash
docker-compose up --build
```

- Dagster UI: http://localhost:3000
- Dashboard: http://localhost:8501

Once the containers are up, open the Dagster UI and materialize all assets to populate the database and dashboard.

## Testing

```bash
pytest tests/
```

## Project Structure

```
.
├── weather_pipeline/
│   ├── definitions.py          # Dagster repository definition
│   └── assets/
│       ├── raw_data.py         # Extraction from Open-Meteo API
│       └── dbt_assets.py       # dbt models exposed as Dagster assets
├── weather_dbt/
│   ├── dbt_project.yml
│   └── models/
│       ├── staging/stg_weather.sql
│       └── marts/mart_daily_weather_stats.sql
├── dashboard/
│   └── app.py
├── tests/
│   └── test_assets.py
├── docker-compose.yml
└── requirements.txt
```
