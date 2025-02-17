from utils.logging_utils import Logger
from utils.performance import measure_performance
import pandas as pd
import os
from returns.pipeline import is_successful
from returns.result import Result, Success, Failure
from config import settings
from utils.io import get_files
from engine.services import writer_service
logger = Logger.setup_logger()
from pandas import DataFrame

column_names = ['Fecha', 'Nemotécnico', 'Precio cierre']
rename_cols = lambda df : df.rename(columns={'Fecha': 'Date', 'Precio cierre': 'Close', 'Nemotécnico':'Stock'})
cast_close = lambda df : df['Close'].astype(str).str.replace(',', '').replace('-', '0').astype(float)
# Cast date column
cast_date = lambda df : pd.to_datetime(df['Date'])




def process_files_in_dir(path, cols, fn) -> DataFrame:
    dfTmp = []
    files = get_files(path, settings.data.landing.bvc_hist.ext)
    for file in files:
        filepath = os.path.join(path, file)
        df = pd.read_csv(filepath, sep=';', names=cols, header=1, usecols=range(len(cols)))
        dfTmp.append(fn(file, df))
    
    return pd.concat(dfTmp, ignore_index=True) if files else None

def process_hist(file, df) -> DataFrame:
    print(f'processing file {file}')
    df = rename_cols(df)    
    df['Close'] = cast_close(df)
    df['Date'] = cast_date(df)
    df.insert(1, 'src', 'hist')
    return df

@measure_performance
def move_landing_to_raw() -> Result[bool, Exception]:

    df = process_files_in_dir(settings.data.landing.bvc_hist.path, column_names, process_hist)
    write_result = writer_service.write(settings.data.raw.bvc_hist.path, df, settings.data.raw.bvc_hist.ext)

    if not is_successful(write_result):
        return write_result.failure()

    return Success(True)


@measure_performance
def run():
    logger.info("bvc hist process")
    landing_result = move_landing_to_raw()
    logger.info("bvc hist has finished successful")

