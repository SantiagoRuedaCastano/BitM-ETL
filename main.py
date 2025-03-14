from pipelines import bvc_daily
from utils.logging_utils import Logger

logger = Logger.setup_logger()


def main():
    bvc_daily.run()


if __name__ == "__main__":
    main()
