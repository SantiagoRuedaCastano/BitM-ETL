import os
from utils.logging_utils import Logger
import csv
from returns.io import IO, IOSuccess, IOFailure, IOResult

logger = Logger.setup_logger()


def get_files(path, extension):
    files = os.listdir(path)
    # Filter only CSV files
    return [file for file in files if file.endswith(f'.{extension}')]

def read_csv_file(input_file:str) -> IOResult[str, str]:
    try:
        # Open the input file and read the content
        with open(input_file, mode='r', newline='', encoding='utf-8') as f:
            return IOSuccess(f.read())
    except IOError as e:
        return IOFailure(input_file)

def write_csv_file(lines:str, file_path:str) -> IOResult[str, str]:
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            f.write(lines)
            
        return IOSuccess(file_path)
    except IOError as e:
        return IOFailure(file_path)

def fix_header(lines:str) -> str:
    return lines.map(lambda line: line.replace(';EQTY', ''))


def fix_csv_file(input_file, output_file) -> IOResult[str, str]:
    match read_csv_file(input_file):
        case IOSuccess(value):
            return write_csv_file(fix_header(value).unwrap(), output_file)
        case _:
            return _
        