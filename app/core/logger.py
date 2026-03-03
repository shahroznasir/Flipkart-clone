from loguru import logger
import sys
import os

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",
)

logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="10 days",
    level="DEBUG",
)
__all__ = ["logger"]