import os
from pathlib import Path

from dynaconf import Dynaconf

setting_file = os.environ.get(
    "SETTINGS", Path(__file__).parent / "settings.json"
)


settings = Dynaconf(
    settings_file=setting_file,
    envvar_prefix="BITM-ETL",
    environments=True,
    load_dotenv=True
)
   