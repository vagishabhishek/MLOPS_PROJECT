
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
from mlops_project.utils.env_loader import load_all_envs
import os
from from_root import from_root
#------------------------------------------------------------------------------
#LOAD ENV FILES
#------------------------------------------------------------------------------
# Auto-load .env during development
# if os.getenv("ENV", "DEV") == "DEV":
#     try:
#         load_all_envs()
#     except Exception as e:
#         print("ENV LOADING ERROR:", e)

if os.getenv("AUTO_LOAD_DOTENV", "0") == "1":
    try:
        load_all_envs()
        print("[ENV LOADER] sucessfully loaded all environment variables.")
    except Exception as e:
        raise


#-----------------------------------------------------------------------------------
# ---------------------- CONFIG ----------------------
LOG_DIR_NAME = "logs"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3

# ---------------------- PATH SETUP ----------------------
root_path = from_root()

LOG_DIR = root_path / LOG_DIR_NAME
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Timestamped log file
LOG_FILE = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.log"

# ---------------------- ROOT LOGGER SETUP ----------------------
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.propagate = False #avoid duplicate records by parent and child loggers

if not root_logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Handler
    fh = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    root_logger.addHandler(fh)

    # Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)

# ---------------------- PUBLIC API ----------------------
def get_logger(name: str = __name__) -> logging.Logger:
    """Return a logger with the given name; defaults to root logger."""
    return logging.getLogger(name) if name else root_logger
