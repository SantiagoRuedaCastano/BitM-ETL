import os

def get_files(path, extension):
    files = os.listdir(path)
    # Filter only CSV files
    return [file for file in files if file.endswith(f'.{extension}')]

def fix_header(filepath):
    pass


