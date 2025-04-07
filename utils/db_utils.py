import duckdb
from utils.logging_utils import Logger

logger = Logger.setup_logger()


class DB:
    _con = None

    @staticmethod
    def setup_db():
        if DB._con:
            return DB._con
        try:

            # Initialize DB
            con = duckdb.connect("./db/BitM.db")
            con.sql("CREATE SCHEMA IF NOT EXISTS landing;")
            con.sql("CREATE SCHEMA IF NOT EXISTS bronze;")
            con.sql("CREATE SCHEMA IF NOT EXISTS silver;")
            con.sql("CREATE SCHEMA IF NOT EXISTS gold;")
            return con
        except Exception as e:
            logger.error(f'Error connecting to DB: {e}')



