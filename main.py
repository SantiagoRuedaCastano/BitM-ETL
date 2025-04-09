from pipelines import bvc_daily, db
from utils.logging_utils import Logger

logger = Logger.setup_logger()


def main():
    db.initialize()
    bvc_daily.run()


if __name__ == "__main__":
    main()
