import logging
from logging.handlers import RotatingFileHandler
import os

# Log directory
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Log file path
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configure the logger
logger = logging.getLogger('AppLogger')
logger.setLevel(logging.DEBUG)

# Create handlers
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=5)
file_handler.setLevel(logging.DEBUG)

# Create formatters and add them to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
