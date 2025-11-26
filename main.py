
from mlops_project.logger import get_logger
from demo import demo_logger

def main():
    logger = get_logger("Main Logger")
    logger.debug("Hello from mlops-project!")
    demo_logger()


if __name__ == "__main__":
    main()
