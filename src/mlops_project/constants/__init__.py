
"""
PROJECT CONSTANTS 
"""
import os
import datetime
from from_root import from_root
from pathlib import Path
from datetime import date

# MongoDB details
DATABASE_NAME = "Proj1"
COLLECTION_NAME = "Proj1-Data"

PIPELINE_NAME : str = "My_Pipeline"
ARTIFACT_DIR : str = "arftifact"

MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "Response"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

FILE_NAME : str = "data.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME : str = "test.csv"
SCHEMA_FILE_PATH = Path("config") / "schema.yaml"

"""
Data Ingetion related constant start with DATA_INGESTION
"""

DATA_INGESTION_COLLECTION_NAME : str = "Proj1-Data"
DATA_INGESTION_DIR_NAME : str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR : str = "feature_store"
DATA_INGESTION_INGESTED_DIR : str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO : float = 0.25


