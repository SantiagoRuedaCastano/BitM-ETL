from utils.performance import measure_performance
from returns.io import IOResult
from returns.result import Result, Success, Failure

from config import settings
from utils.db_utils import DB
from utils.io import *
from utils.performance import measure_performance
from core.error_context import ErrorType, ErrorInfo
from pathlib import Path
import re

logger = Logger.setup_logger()
conn = DB.setup_db()


def extract_date_from_file_name(file_name):
    
    # Regular expression pattern
    pattern = r'RVLocal_(\d{4})(\d{2})(\d{2})\.csv'
    
    # Search for the pattern in the string
    match = re.search(pattern, file_name)
    
    # Extract the matched groups
    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        return f"{year}-{month}-{day}"

    return '1970-01-01'    

@measure_performance
def load(file_path, date_str) -> Result[str, ErrorInfo]:
    try:
        logger.info('Loading the file into landing stage')
        table = settings.data.landing.bvc_daily.table
        conn.query(
            f"""
            CREATE OR REPLACE TABLE {table} AS
            SELECT 
                '{date_str}'::DATE as Date,
                *,
                CURRENT_LOCALTIMESTAMP() AS UPDATED_AT
            FROM read_csv('{file_path}', delim = ';', header = true);
            """
        )
        return Success(table)
    except Exception as e:
        return Failure(ErrorInfo(ErrorType.ERROR_LOADING_LANDING, e))

def extract(path_file) -> Result[str, ErrorInfo]:
        return fix_csv_file(path_file, path_file)



@measure_performance
def transform(src:str, date_str) -> Result[str, ErrorInfo]:
    try:
        table = settings.data.bronze.bvc_daily.table

        conn.query(
            f"""
            INSERT INTO TABLE {table}
            SELECT
                DATE,
                "Nemotécnico" AS STOCK,
                "Volúmenes" AS VOL,
                Cantidad AS QTY,
                "Precio apertura" AS OPEN,
                "Precio máximo" AS HIGH,
                "Precio mínimo" AS LOW,
                "Último precio" AS CLOSE,
                UPDATED_AT
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
        date_str = extract_date_from_file_name(file)

        logger.info(extract(input_file)
            .bind(lambda filepath: load(filepath, date_str))
            .bind(lambda table: transform(table, date_str)))

        match move_file(input_file, output_file):
            case IOSuccess(_):
                logger.info(f'File has been processed successfully: {input_file}')
            case IOFailure(value):
                logger.error(value)
        

   