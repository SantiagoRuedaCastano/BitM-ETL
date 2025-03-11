import os
from utils.logging_utils import Logger
import csv

logger = Logger.setup_logger()


def get_files(path, extension):
    files = os.listdir(path)
    # Filter only CSV files
    return [file for file in files if file.endswith(f'.{extension}')]

def fix_header(input_file) -> bool:

    logger.info(input_file)

    # Open the input file and read the content
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    # Modify the header (first line)
    header = rows[0]
    header = [column.replace("Emisor / nombre", "Emisor;Equity") for column in header]

    # Write the modified content to the output file without adding extra quotes
    with open(input_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_NONE)
        writer.writerows([header] + rows[1:])  # Write the modified header followed by the rest of the data


