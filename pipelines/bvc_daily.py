from utils.logging_utils import Logger
from utils.performance import measure_performance
from utils.io import *
import functools
from config import settings
from pathlib import Path
from returns.io import IO, IOSuccess, IOFailure, IOResult

logger = Logger.setup_logger()

def fix_files(path, ext):
    for file in get_files(path, ext):
        path_file = Path(path) / file
        match fix_csv_file(path_file, path_file):
            case IOSuccess(value):
                logger.info(f'File {value} was processed')
            case IOFailure(value):
                logger.error(f'Error processing File {value}')


@measure_performance
def run():
    logger.info("bvc daily process")
    fix_files(settings.data.landing.bvc_daily.path, settings.data.landing.bvc_daily.ext)
