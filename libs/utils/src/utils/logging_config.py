"""Logging configuration utilities shared across services."""

import logging
import sys
from typing import Optional


def setup_logger(name: str, level: str = "INFO",
                format_string: Optional[str] = None) -> logging.Logger:
    """Set up a standardized logger for services."""
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(format_string)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def log_request_info(logger: logging.Logger, method: str, path: str,
                    status_code: int, duration: float):
    """Log HTTP request information in standardized format."""
    logger.info(f"{method} {path} - {status_code} - {duration:.3f}s")


def log_data_processing_stats(logger: logging.Logger, operation: str,
                            records_processed: int, duration: float):
    """Log data processing statistics."""
    rate = records_processed / duration if duration > 0 else 0
    logger.info(f"{operation}: {records_processed} records in {duration:.2f}s "
                f"({rate:.1f} records/sec)")
