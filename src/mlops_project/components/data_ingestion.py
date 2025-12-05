import os
import sys
import pandas as pd

from sklearn.model_selection import train_test_split
from mlops_project.entity.config_entity import DataIngestionConfig
from mlops_project.entity.artifact_entity import DataIngestionArtifact
from mlops_project.exception import MyException
from mlops_project.logger import get_logger
from mlops_project.data_access.mlops_proj_data import ProjData


class DataIngetion:
    """
    Main class responsible for:
    1. Fetching data from MongoDB
    2. Splitting into train/test
    3. Saving train/test CSV files
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e, sys)

    # -------------------------------------------------------------------------
    def export_data_into_feature_store(self) -> pd.DataFrame:
        """
        Fetches data from MongoDB and returns it as a pandas DataFrame.
        IMPORTANT: Your earlier code was missing `return dataframe`.
        """
        logger = get_logger("ExportData")
        logger.info("Fetching data from MongoDB...")

        try:
            my_data = ProjData()

            # Fetch MongoDB data
            dataframe = my_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )

            # Safety check — NONE
            if dataframe is None:
                raise MyException("MongoDB returned None instead of DataFrame.", sys)

            # Safety check — EMPTY DF
            if dataframe.empty:
                raise MyException("MongoDB returned empty DataFrame.", sys)

            logger.info(f"Shape of DataFrame fetched: {dataframe.shape}")

            # THE MAIN FIX — RETURN THE DATAFRAME
            return dataframe

        except Exception as e:
            raise MyException(e, sys)

    # -------------------------------------------------------------------------
    def split_data_as_train_test_split(self, dataframe: pd.DataFrame) -> None:
        """
        Takes DataFrame and splits into train and test CSV files.
        """
        logger = get_logger("DataSplit")
        logger.info("Starting train-test split...")

        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logger.info("Train-test split complete.")

            # Create folder if needed
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # Save files
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False)

            logger.info("Train and test CSV files saved successfully.")

        except Exception as e:
            raise MyException(e, sys)

    # -------------------------------------------------------------------------
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Main Orchestrator:
        1. Fetch DF
        2. Split DF
        3. Return artifact
        """
        logger = get_logger("Ingestion")
        logger.info("Initiating Data Ingestion Pipeline...")

        try:
            # STEP 1 → Fetch DF
            dataframe = self.export_data_into_feature_store()
            logger.info(f"DataFrame received in pipeline: {type(dataframe)}")

            # STEP 2 → Split DF
            self.split_data_as_train_test_split(dataframe)

            # STEP 3 → Prepare Artifact
            artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logger.info(f"Data Ingestion Artifact Created: {artifact}")
            return artifact

        except Exception as e:
            raise MyException(e, sys)
