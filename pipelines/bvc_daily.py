from utils.performance import measure_performance
from returns.io import IOResult
from returns.result import Result, Success, Failure

from config import settings
from utils.db_utils import DB
from utils.io import *
from utils.performance import measure_performance

logger = Logger.setup_logger()
conn = DB.setup_db()

@measure_performance
def load(file_path) -> Result[str, str]:
    try:
        table = {settings.data.landing.bvc_daily.table}
        conn.query(
            f"""
            CREATE OR REPLACE TABLE {table} AS
            SELECT 
            *
            FROM read_csv('{file_path}', delim = ';', header = true);
            """
        )
        return Success(table)
    except Exception as e:
        return Failure(str(e))

def extract(path_file) -> Result[str, str]:
        return fix_csv_file(path_file, path_file)



@measure_performance
def transform(table:str) -> Result[str, str]:
    try:

        conn.query(
            f"""
            CREATE OR REPLACE TABLE {table} AS
            SELECT
                "Nemotécnico" AS Stock,
                "Volúmenes" AS Vol,
                Cantidad AS Qty,
                "Precio apertura" AS Open,
                "Precio máximo" AS High,
                "Precio mínimo" AS Low,
                "Último precio" AS Close
            FROM {table};
            """
        )
        return Success(table)
    except Exception as e:
        return Failure(str(e))

@measure_performance
def run():
    logger.info("bvc daily process")
    dir_path = settings.data.landing.bvc_daily.path
    for file in get_files(dir_path, settings.data.landing.bvc_daily.ext):
        extract(file).bind(load)

   