import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from from_root import from_root
from urllib.parse import quote_plus
from mlops_project.logger import get_logger
from mlops_project.exception import MyExcption


def create_mongo_uri():
    """
    Read MongoDB credentials from .env/mongo_cred.env and create a connection URI.

    Expects the following variables in mongo_cred.env:
      - MONGO_USER
      - MONGO_PASSWORD
      - MONGO_HOST
      - CLUSTER

    Returns:
        str: MongoDB connection URI

    Raises:
        MyExcption: if directory, file, or env variables are missing
    """
    logger = get_logger("MongoDB URL Creation")

    try:
        PROJECT_ROOT = Path(from_root())
        logger.info("PROJECT_ROOT set.")

        ENV_PATH = PROJECT_ROOT / ".env"
        MONGO_CRED_PATH = ENV_PATH / "mongo_cred.env"

        # Check if directory exists
        if not ENV_PATH.exists():
            raise FileNotFoundError(f".env directory not found at: {ENV_PATH}")

        # Check if file exists
        if not MONGO_CRED_PATH.exists():
            raise FileNotFoundError(f"mongo_cred.env not found at: {MONGO_CRED_PATH}")

        # Load environment variables
        load_dotenv(MONGO_CRED_PATH)
        logger.info("Environment variables loaded from mongo_cred.env")

        # Get raw variables
        MONGO_USER_RAW = os.getenv("MONGO_USER")
        MONGO_PASSWORD_RAW = os.getenv("MONGO_PASSWORD")
        MONGO_HOST = os.getenv("MONGO_HOST")
        MONGO_CLUSTER = os.getenv("CLUSTER")

        # Validate missing fields
        if not all([MONGO_USER_RAW, MONGO_PASSWORD_RAW, MONGO_HOST, MONGO_CLUSTER]):
            raise ValueError(
                "Some or all env fields missing. SET MONGO_USER, MONGO_PASSWORD, MONGO_HOST, CLUSTER"
            )

        # Encode credentials
        MONGO_USER = quote_plus(MONGO_USER_RAW)
        MONGO_PASSWORD = quote_plus(MONGO_PASSWORD_RAW)

        mongo_uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/?appName={MONGO_CLUSTER}"
        logger.info("MongoDB URI created successfully.")

        return mongo_uri

    except FileNotFoundError as e:
        logger.error(f"File or directory missing: {e}", exc_info=True)
        raise MyExcption(str(e), sys)

    except ValueError as e:
        logger.error(f"Invalid or missing environment values: {e}", exc_info=True)
        raise MyExcption(str(e), sys)

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise MyExcption(str(e), sys)
