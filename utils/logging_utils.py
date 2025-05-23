from loguru import logger
import sys
from config import settings


class Logger:
    _logger = None

    @staticmethod
    def setup_logger():
        if Logger._logger:
            return Logger._logger

        # Configure logging levels
        logger.remove()  # Remove the default configuration
        logger.add(sink=settings.logging.debug.sink,
                   level=settings.logging.debug.level,
                   format=settings.logging.debug.format)  # Log to a file with DEBUG level

        logger.add(sink=eval(settings.logging.info.sink),
                   level=settings.logging.info.level,
                   format=settings.logging.info.format,
                   colorize=True)  # Log to sys.stdout with INFO level

        return logger



