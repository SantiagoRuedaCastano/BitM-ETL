from enum import Enum
from dataclasses import dataclass

class ErrorType(Enum):
    FILE_NOT_FOUND = 'File not found'
    ANOTHER_ERROR_NO_IDENTIFIED = 'Error no identified'
    ERROR_LOADING_LANDING = 'Error loading the file in the landing stage'

@dataclass(frozen=True)
class ErrorInfo:
    error_type: ErrorType
    exception: Exception