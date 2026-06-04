import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger for the application."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create console handler with a higher log level
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger
