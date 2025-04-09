from utils.performance import measure_performance
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


def initialize_bronze_layer() -> Result[str, ErrorInfo]:

    try:
        logger.info('Initializing bronze stage')
        table = settings.data.bronze.bvc_daily.table
        conn.query(
            f"""
                CREATE TABLE IF NOT EXISTS {table}
                (
                    DATE DATE NOT NULL,
                    STOCK VARCHAR,
                    VOL VARCHAR,
                    QTY BIGINT,
                    OPEN VARCHAR,
                    HIGH VARCHAR,
                    LOW VARCHAR,
                    CLOSE VARCHAR,
                    UPDATED_AT TIMESTAMP NOT NULL
                );
            """
        )
        return Success(f'Table initalized successful: {table}')
    except Exception as e:
        return Failure(ErrorInfo(ErrorType.ERROR_INITIALIZING_DB, e))


@measure_performance
def initialize():

    logger.info(f'Initialize DB has finished with status: {initialize_bronze_layer()}')
