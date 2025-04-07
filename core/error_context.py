from enum import Enum
from dataclasses import dataclass

class ErrorType(Enum):
    FILE_NOT_FOUND = 'File not found'
    ANOTHER_ERROR_NO_IDENTIFIED = 'Error no identified'
    ERROR_LOADING_LANDING = 'Error loading the file in the landing stage'
    ERROR_TRANSFORMING_DATA = 'Error transforming data in bronze stage'
    ERROR_MOVING_FILE = 'Error moving the file'
    ERROR_INITIALIZING_DB = 'it has occurred an issue initializing the db.'

@dataclass(frozen=True)
class ErrorInfo:
    error_type: ErrorType
    exception: Exception