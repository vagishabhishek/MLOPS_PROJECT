import os
import sys
import pymongo
import certifi

from mlops_project.exception import MyException
from mlops_project.logger import get_logger
from mlops_project.constants import DATABASE_NAME
from mlops_project.utils.mongo_utils import create_mongo_uri

# Load trusted CA certificate for secure MongoDB Atlas connection
ca = certifi.where()


class MongoClient:
    """
    A Singleton-style MongoDB client manager.

    This class establishes and maintains **one shared MongoDB connection**
    across the entire application.

    NOTES
    -----
    - This class **does NOT load `.env` files**.
      Environment variables must already be loaded globally
      (which logger handles automatically if AUTO_LOAD_DOTENV=1).

    - MongoDB credentials must be available via:
        MONGO_USER, MONGO_PASSWORD, MONGO_HOST, CLUSTER

    Attributes
    ----------
    client : pymongo.MongoClient or None
        A shared singleton MongoDB client instance.

    database : pymongo.database.Database
        Reference to the active database within MongoDB.
    """

    # Shared Mongo client (singleton instance for entire app)
    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initialize MongoDB connection and select the target database.

        Parameters
        ----------
        database_name : str
            Name of the MongoDB database to connect to.

        Raises
        ------
        MyException
            - If environment variables are missing.
            - If URI creation fails.
            - If connection to MongoDB fails.
        """
        logger = get_logger("MongoDB Connection")

        try:
            # Build URI from environment variables
            mongo_db_uri = create_mongo_uri()

            if not mongo_db_uri:
                raise MyException(
                    "MongoDB URI creation failed. Missing required environment variables.",
                    sys
                )

            # Create new client only once (singleton)
            if MongoClient.client is None:
                logger.info("Creating a new MongoDB client...")

                MongoClient.client = pymongo.MongoClient(
                    mongo_db_uri,
                    tlsCAFile=ca,  # fixes SSL CERTIFICATE_VERIFY_FAILED issues
                )

                logger.info("MongoDB client created successfully.")

            else:
                logger.info("Reusing existing MongoDB client.")

            # Get database (PyMongo 4.x compatible)
            self.database = MongoClient.client.get_database(database_name)

            logger.info(f"Connected to database: {database_name}")

        except Exception as e:
            raise MyException(e, sys)
