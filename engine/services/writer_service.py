from returns.result import Result
from utils.logging_utils import Logger
from pandas import DataFrame
from returns.result import Result, Success, Failure

logger = Logger.setup_logger()



def write_parquet(path: str, df: DataFrame) -> Result[bool, Exception]:
    try:
        logger.info(f"writing to path: {path}")
        df.to_parquet(path)
    except Exception as e:
        logger.error(f"Error writing to path: {path}. {e}")
        return Failure(e)

    return Success(True)



def write(path: str, df: DataFrame, extension:str) -> Result[bool, Exception]:
    match extension:
        case 'parquet':
            return write_parquet(path, df)
        case _ :
            return Failure(Exception(f'writer for {_} has not been implemented'))
