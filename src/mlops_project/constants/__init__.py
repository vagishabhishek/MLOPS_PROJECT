
"""
PROJECT CONSTANTS
"""
import os
import datetime
from from_root import from_root
from pathlib import Path
from mlops_project.utils.mongo_utils import create_mongo_uri


PROJECT_ROOT = Path(from_root())
ENV_PATH = PROJECT_ROOT / ".env"


MONGO_CRED_PATH = ENV_PATH / "mongo_cred.env"
MONGODB_URL_KEY = create_mongo_uri()
DATABASE_NAME = "Proj1"
COLLECTION_NAME = "Proj1-Data"

