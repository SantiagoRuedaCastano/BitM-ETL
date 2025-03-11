from utils.logging_utils import Logger
from utils.performance import measure_performance
from utils.io import *
import functools
from config import settings
from pathlib import Path

logger = Logger.setup_logger()

def fix_files(path, ext):
    for file in get_files(path, ext):
        fix_header(Path(path) / file)

    logger.info(f'done...')
    

@measure_performance
def run():
    logger.info("bvc daily process")
    fix_files(settings.data.landing.bvc_daily.path, settings.data.landing.bvc_daily.ext)
