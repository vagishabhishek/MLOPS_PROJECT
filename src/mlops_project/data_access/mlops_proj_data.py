import sys
import pandas as pd
import numpy as np
from typing import Optional

from mlops_project.configuration.mongo_db_connection import MongoClient
from mlops_project.constants import DATABASE_NAME
from mlops_project.exception import MyException
from mlops_project.logger import get_logger

logger = get_logger("MongoDB->DataFrame Loader")


class ProjData:
    """
    Utility class to fetch MongoDB collections as Pandas DataFrames.

    - Uses the shared MongoDB client (singleton pattern).
    - Handles missing collections, empty results, and dataframe cleanup.
    """

    def __init__(self) -> None:
        """Initialize DB connection using global MongoClient."""
        try:
            self.mongo_client = MongoClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)

    def export_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch a MongoDB collection and convert it into a clean pandas DataFrame.

        Parameters
        ----------
        collection_name : str
            Name of the MongoDB collection.
        database_name : Optional[str]
            If provided, overrides default database name.

        Returns
        -------
        pd.DataFrame
            The fetched collection as a DataFrame.

        Raises
        ------
        MyException
            For missing collections, connection errors, or data conversion issues.
        """
        try:
            # Select database (default or overridden)
            db = (
                self.mongo_client.client.get_database(database_name)
                if database_name
                else self.mongo_client.database
            )

            # Select collection (PyMongo 4.x)
            collection = db.get_collection(collection_name)

            logger.info(f"Fetching data from MongoDB collection: {collection_name}")

            # Convert cursor → list → DataFrame
            documents = list(collection.find())

            if not documents:
                logger.warning(
                    f"No documents found in collection '{collection_name}'. Returning empty DataFrame."
                )
                return pd.DataFrame()

            df = pd.DataFrame(documents)

            logger.info(f"Data fetched successfully. Row count = {len(df)}")

            # Cleanup: Remove Mongo's default _id
            if "_id" in df.columns:
                df.drop("_id", axis=1, inplace=True)

            # Replace 'na' strings with NaN
            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise MyException(e, sys)


if __name__ == "__main__":
    import logging
    #set_level = logging.CRITCAL to silence pymongo undesired logs
    get_logger("pymongo").setLevel(logging.CRITICAL)
    from mlops_project.constants import COLLECTION_NAME

    data = ProjData()
    df = data.export_collection_as_dataframe(COLLECTION_NAME, DATABASE_NAME)
    logger.info(f"""\n
                {df.head()}""")
