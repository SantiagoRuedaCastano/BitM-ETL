from utils.logging_utils import Logger
from utils.performance import measure_performance
from utils.io import *
import functools
from config import settings
from pathlib import Path
from returns.maybe import Maybe, Some, Nothing

logger = Logger.setup_logger()

def fix_files(path, ext) -> List[Maybe[Path]]:
    return List(map(lambda file: fix_header(Path(path) / file), get_files(path, ext)))


@measure_performance
def run():
    logger.info("bvc daily process")
    fix_files(settings.data.landing.bvc_daily.path, settings.data.landing.bvc_daily.ext)
