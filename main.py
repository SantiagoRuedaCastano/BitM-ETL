from engine.orchestrators import app_orchestrator
from utils.logging_utils import Logger

logger = Logger.setup_logger()


def main():
    app_orchestrator.run()


if __name__ == "__main__":
    main()
