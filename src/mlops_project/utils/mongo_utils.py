"""
MongoDB connection URI builder.

Environment variables required:
    - MONGO_USER
    - MONGO_PASSWORD
    - MONGO_HOST
    - CLUSTER

These should be provided from:
    - Real production environment variables
    - Loaded automatically by logger (if AUTO_LOAD_DOTENV=1)
    - Or set manually during unit tests

This module does NOT load .env files. It simply reads environment variables.
"""

import os
from urllib.parse import quote_plus
from mlops_project.logger import get_logger
from mlops_project.exception import MyException
import sys

# ---------------------- LOGGER ----------------------
logger = get_logger("MongoURI")


# ---------------------- FUNCTION ----------------------
def create_mongo_uri() -> str:
    """
    Create a MongoDB connection URI using environment variables.

    Behavior:
        - Reads required environment variables.
        - Prompts an error if any required variables are missing.
        - Encodes credentials safely for MongoDB URI.

    Required environment variables:
        - MONGO_USER
        - MONGO_PASSWORD
        - MONGO_HOST
        - CLUSTER

    Returns:
        str: MongoDB connection URI in the form:
             mongodb+srv://<user>:<password>@<host>/?appName=<cluster>

    Raises:
        MyException: If any required environment variables are missing or other errors occur.
    """
    try:
        # ---------------------- CHECK ENVIRONMENT VARIABLES ----------------------
        required_vars = ["MONGO_USER", "MONGO_PASSWORD", "MONGO_HOST", "CLUSTER"]
        missing_vars = [v for v in required_vars if os.getenv(v) is None]

        if missing_vars:
            msg = (
                f"Missing required environment variables: {missing_vars}\n"
                "Please provide them in the system environment or in a .env file "
                "with the following format:\n"
                "MONGO_USER=your_user\n"
                "MONGO_PASSWORD=your_password\n"
                "MONGO_HOST=your_cluster_host\n"
                "CLUSTER=your_cluster_name"
            )
            logger.error(msg)
            # Raise MyException with error detail
            raise MyException(msg, sys)

        # ---------------------- BUILD MONGO URI ----------------------
        user = quote_plus(os.getenv("MONGO_USER"))
        password = quote_plus(os.getenv("MONGO_PASSWORD"))
        host = os.getenv("MONGO_HOST")
        cluster = os.getenv("CLUSTER")

        mongo_uri = f"mongodb+srv://{user}:{password}@{host}/?appName={cluster}"

        logger.info("MongoDB URI successfully created.")
        return mongo_uri

    except Exception as e:
        # Wrap all exceptions in MyException
        raise MyException(e, sys)
