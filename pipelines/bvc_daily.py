from utils.logging_utils import Logger
from utils.performance import measure_performance

logger = Logger.setup_logger()

@measure_performance
def run():
    logger.info("bvc daily process")
    io.fix_header(settings.data.landing.bvc_daily.path)
