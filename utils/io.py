import os
from utils.logging_utils import Logger
import csv
from returns.io import IO, IOSuccess, IOFailure, IOResult

logger = Logger.setup_logger()


def get_files(path, extension):
    files = os.listdir(path)
    # Filter only CSV files
    return [file for file in files if file.endswith(f'.{extension}')]


def read_csv_file(input_file) -> IOResult[str, str]:
    try:
        # Open the input file and read the content
        with open(input_file, mode='r', newline='', encoding='utf-8') as f:
            return IOSuccess(f.read())
    except IOError as e:
        return IOFailure(input_file)
            

def write_csv_file(output_file) -> IOResult[str, str]:
    try:
        # Write the modified content to the output file without adding extra quotes
        with open(input_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_NONE)
            writer.writerows([header] + rows[1:]) 
            
        return IOSuccess[output_file]
    except IOError as e:
        return IOFailure(output_file)



def fix_header(input_file) -> IOResult[str, str] :
    return read_csv_file(input_file).map(write_csv_file)
