import os
import sys
import pymongo
import certifi

from mlops_project.exception import MyExcption
from mlops_project.logger import get_logger
from mlops_project.constants import DATABASE_NAME

# Load trusted CA certificates (prevents SSL CERTIFICATE_VERIFY_FAILED)
ca = certifi.where()


class MongoClient:
    """
    MongoClient class is responsible for creating and maintaining a single
    shared MongoDB connection across the application.

    This class DOES NOT load .env files.
    The application entry point (main.py, app.py, etc.) must call load_dotenv().

    Attributes
    ----------
    client : pymongo.MongoClient or None
        Shared Mongo client instance created once and reused.

    database : pymongo.database.Database
        A reference to the specific MongoDB database.
    """

    # Shared connection (singleton)
    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initialize and connect to the MongoDB database.

        Parameters
        ----------
        database_name : str
            Name of the database to connect to.

        Raises
        ------
        MyExcption
            If the MongoDB URI is missing or connection fails.
        """
        logger = get_logger("MongoDB Connection")

        try:
            # Read connection string from environment variable
            mongo_db_uri = os.getenv("MONGO_DB_URI")

            # If MongoDB URI is not present → raise an error
            if not mongo_db_uri:
                logger.error("Environment variable MONGO_URI is missing.")
                raise MyExcption("MONGO_URI not found. Did you load .env?", sys)

            # If no client exists → create a new connection
            if MongoClient.client is None:
                logger.info("Creating a new MongoDB client...")
                MongoClient.client = pymongo.MongoClient(
                    mongo_db_uri,
                    tlsCAFile=ca  # ensures proper SSL authentication
                )
                logger.info("MongoDB client created successfully.")

            # Re-use existing client
            logger.info("Using existing MongoDB client.")
            self.database = MongoClient.client[database_name]
            logger.info(f"Connected to database: {database_name}")

        except Exception as e:
            # Wrap all errors in your custom exception
            raise MyExcption(e, sys)


