import os
import pandas as pd
import requests
from sqlalchemy import create_engine
from dagster import asset

@asset
def raw_weather() -> None:
    """Fetches weather data from Open-Meteo and stores it in PostgreSQL."""
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2026-03-24&end_date=2026-04-07&hourly=temperature_2m"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temperatures = hourly.get("temperature_2m", [])
    
    df = pd.DataFrame({
        "time": times,
        "temperature_2m": temperatures
    })
    
    # Configuration PostgreSQL
    host = os.environ.get("POSTGRES_HOST", "localhost")
    user = os.environ.get("POSTGRES_USER", "weather_user")
    password = os.environ.get("POSTGRES_PASSWORD", "weather_pass")
    dbname = os.environ.get("POSTGRES_DB", "weather_db")
    
    db_url = f"postgresql://{user}:{password}@{host}:5432/{dbname}"
    engine = create_engine(db_url)
    
    # Store into PostgreSQL (remplace si existe)
    df.to_sql('raw_weather', con=engine, if_exists='replace', index=False)
