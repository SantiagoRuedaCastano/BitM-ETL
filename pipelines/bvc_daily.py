from utils.performance import measure_performance
from returns.io import IOResult
from returns.result import Result, Success, Failure

from config import settings
from utils.db_utils import DB
from utils.io import *
from utils.performance import measure_performance
from core.error_context import ErrorType, ErrorInfo
from pathlib import Path

logger = Logger.setup_logger()
conn = DB.setup_db()




@measure_performance
def load(file_path) -> Result[str, ErrorInfo]:
    try:
        logger.info('Loading the file into landing stage')
        table = settings.data.landing.bvc_daily.table
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
        return Failure(ErrorInfo(ErrorType.ERROR_LOADING_LANDING, e))

def extract(path_file) -> Result[str, ErrorInfo]:
        return fix_csv_file(path_file, path_file)



@measure_performance
def transform(src:str) -> Result[str, ErrorInfo]:
    try:
        table = settings.data.bronze.bvc_daily.table

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
            FROM {src};
            """
        )
        return Success(table)
    except Exception as e:
        return Failure(ErrorInfo(ErrorType.ERROR_TRANSFORMING_DATA, e))

@measure_performance
def run():
    logger.info("bvc daily process")
    dir_path = settings.data.landing.bvc_daily.path
    processed_path = settings.data.landing.bvc_daily.path_processed
    for file in get_files(dir_path, settings.data.landing.bvc_daily.ext):
        input_file = Path(dir_path, file)
        output_file = Path(processed_path, file)
        logger.info(extract(input_file).bind(load).bind(transform))

        match move_file(input_file, output_file):
            case IOSuccess(_):
                logger.info(f'File has been processed successfully: {input_file}')
            case IOFailure(value):
                logger.error(value)
        

   