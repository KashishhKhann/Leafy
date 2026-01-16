import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Create logger
logger = logging.getLogger('Leafy')
logger.setLevel(logging.DEBUG)

# Log file path
log_file = os.path.join(LOGS_DIR, f"leafy_{datetime.now().strftime('%Y%m%d')}.log")

# Create file handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_command(command, status="executed"):
    """Log voice commands."""
    logger.info(f"[COMMAND] {command} - Status: {status}")


def log_error(error_type, error_message, details=""):
    """Log errors with context."""
    logger.error(f"[{error_type}] {error_message} | Details: {details}")


def log_info(message):
    """Log general information."""
    logger.info(f"[INFO] {message}")
