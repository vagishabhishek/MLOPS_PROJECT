import os
import sys
import pymongo
import certifi

from mlops_project.exception import MyExcption
from mlops_project.logger import get_logger
from mlops_project.constants import DATABASE_NAME,MONGODB_URL_KEY
