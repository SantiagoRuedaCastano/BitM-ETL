import os

from returns.io import IOSuccess, IOFailure, IOResult
from returns.result import Result

from utils.logging_utils import Logger

logger = Logger.setup_logger()

from core.error_context import ErrorType, ErrorInfo

def get_files(path, extension):
    files = os.listdir(path)
    # Filter only CSV files
    return [file for file in files if file.endswith(f'.{extension}')]

def read_csv_file(input_file:str) -> IOResult[str, ErrorInfo]:
    try:
        # Open the input file and read the content
        with open(input_file, mode='r', newline='', encoding='utf-8') as f:
            return IOSuccess(f.read())
    except IOError as e:
        return IOFailure(ErrorInfo(ErrorType.FILE_NOT_FOUND, e))

def write_csv_file(lines:str, file_path:str) -> IOResult[str, ErrorType]:
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            f.write(lines)
            
        return IOSuccess(file_path)
    except IOError as e:
        return IOFailure(ErrorInfo(ErrorType.ANOTHER_ERROR_NO_IDENTIFIED, e))

def fix_header(lines:str) -> str:
    return lines.replace(';EQTY', '')


def fix_csv_file(input_file, output_file) -> Result[str, ErrorInfo]:
    return read_csv_file(input_file).bind(lambda value:  write_csv_file(fix_header(value), output_file))
        