from functools import reduce
from engine.factories.pipeline_factory import get_pipeline
from config import settings
from utils.logging_utils import Logger

logger = Logger.setup_logger()


def run():

    logger.info(f'Starting the processing with the following steps: {settings.engine.steps}')

    try:
        
        reduce(lambda _, f: f(), map(get_pipeline, settings.engine.steps), None)

    except Exception as e:
        logger.error(f'Error during processing: {str(e)}')

    finally:
        logger.info(f'The process has finalized')
