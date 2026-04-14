import os
from pathlib import Path
from dagster_dbt import DbtCliResource, dbt_assets

dbt_project_dir = Path(__file__).joinpath("..", "..", "..", "weather_dbt").resolve()
dbt = DbtCliResource(project_dir=os.fspath(dbt_project_dir))

dbt.cli(["deps"], target_path=Path("target")).wait()
# Dagster recommends parsing dbt project at definition time
dbt_parse_invocation = dbt.cli(["parse"], target_path=Path("target")).wait()

@dbt_assets(manifest=dbt_parse_invocation.target_path.joinpath("manifest.json"))
def weather_dbt_assets(context):
    yield from dbt.cli(["build"], context=context).stream()
