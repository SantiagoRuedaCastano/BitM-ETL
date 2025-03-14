import duckdb


class DB:
    _con = None

    @staticmethod
    def setup_db():
        if DB._con:
            return DB._con

        # Initialize DB
        con = duckdb.connect("./db/BitM.db")
        con.sql("CREATE SCHEMA IF NOT EXISTS landing;")
        con.sql("CREATE SCHEMA IF NOT EXISTS bronze;")
        con.sql("CREATE SCHEMA IF NOT EXISTS silver;")
        con.sql("CREATE SCHEMA IF NOT EXISTS gold;")
        return con



