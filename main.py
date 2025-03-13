from utils.logging_utils import Logger
from pipelines import bvc_daily

logger = Logger.setup_logger()


def main():
    bvc_daily.run()


if __name__ == "__main__":
    main()
