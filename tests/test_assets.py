import pytest
from unittest.mock import patch, MagicMock
from weather_pipeline.assets.raw_data import raw_weather
import pandas as pd

@patch("weather_pipeline.assets.raw_data.pd.DataFrame.to_sql")
@patch("weather_pipeline.assets.raw_data.create_engine")
@patch("weather_pipeline.assets.raw_data.requests.get")
def test_raw_weather_asset(mock_get, mock_engine, mock_to_sql):
    """Teste l'extraction de l'API et l'insertion dans Postgres de l'asset raw_weather."""
    
    # Configuration du mock pour l'API
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "hourly": {
            "time": ["2026-03-24T00:00", "2026-03-24T01:00"],
            "temperature_2m": [6.4, 4.5]
        }
    }
    mock_get.return_value = mock_response
    
    mock_eng_instance = MagicMock()
    mock_engine.return_value = mock_eng_instance
    
    # Exécution de l'asset Dagster
    raw_weather()
    
    # Vérifications
    mock_get.assert_called_once()
    mock_engine.assert_called_once()
    mock_to_sql.assert_called_once_with('raw_weather', con=mock_eng_instance, if_exists='replace', index=False)
