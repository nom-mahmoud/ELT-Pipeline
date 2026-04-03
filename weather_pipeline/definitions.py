from dagster import Definitions, load_assets_from_modules, define_asset_job, ScheduleDefinition
from dagster_dbt import DbtCliResource
import os

from weather_pipeline.assets import raw_data, dbt_assets
from pathlib import Path

dbt_project_dir = Path(__file__).joinpath("..", "..", "weather_dbt").resolve()

all_assets = load_assets_from_modules([raw_data, dbt_assets])

weather_job = define_asset_job(
    name="weather_pipeline_job",
    selection="*",
)

daily_schedule = ScheduleDefinition(
    job=weather_job,
    cron_schedule="0 8 * * *", # Run daily at 8 AM
)

defs = Definitions(
    assets=all_assets,
    jobs=[weather_job],
    schedules=[daily_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir))
    }
)
