import time
from functools import wraps

from utils.logging_utils import Logger

logger = Logger.setup_logger()


def measure_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling the function {func.__name__} with args: {args}, kwargs: {kwargs}")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Function {func.__name__} Execution time: {round((end_time - start_time) * 1000, 3)} ms")
        return result

    return wrapper
