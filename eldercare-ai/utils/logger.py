import logging
import os
from logging.handlers import RotatingFileHandler

# Configure the logger
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logger = logging.getLogger("EldercareAI")
logger.setLevel(getattr(logging, log_level, logging.INFO))

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# File Handler with rotation
log_dir = "logs"
try:
    os.makedirs(log_dir, exist_ok=True)
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "eldercare_ai.log"),
        maxBytes=1024*1024,  # 1 MB per file
        backupCount=3,       # Keep 3 backup files
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
except PermissionError as e:
    logger.warning(f"Could not create file handler due to permission error: {e}")
except Exception as e:
    logger.error(f"Error setting up file handler: {e}")

# Avoid duplicate handlers
if not logger.hasHandlers():
    logger.addHandler(console_handler)
    if 'file_handler' in locals():
        logger.addHandler(file_handler)