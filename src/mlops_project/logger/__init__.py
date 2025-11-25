import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
from from_root import from_root

# ---------------------- CONFIG ----------------------
LOG_DIR = "logs"
LOG_FILE = f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log'
MAX_LOG_SIZE = 5 * 1024 * 1024   # 5 MB
BACKUP_COUNT = 3

# ---------------------- PATH SETUP ----------------------
log_dir = Path(from_root()) / LOG_DIR
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / LOG_FILE

# ---------------------- ROOT LOGGER SETUP ----------------------
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

if not root_logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | "
        "%(filename)s:%(lineno)d | %(message)s"
    )

    # File Handler
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)

# ---------------------- PUBLIC API ----------------------
def get_logger(name: str = None):
    """Return logger with correct name and inherited handlers."""
    return logging.getLogger(name)
