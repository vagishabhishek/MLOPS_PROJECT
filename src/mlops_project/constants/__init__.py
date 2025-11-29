
"""
PROJECT CONSTANTS
"""
import os
import datetime
from from_root import from_root
from pathlib import Path


PROJECT_ROOT = Path(from_root())
ENV_PATH = PROJECT_ROOT / ".env"


MONGO_CRED_PATH = ENV_PATH / "mongo_cred.env"
DATABASE_NAME = "Proj1"
COLLECTION_NAME = "Proj1-Data"


