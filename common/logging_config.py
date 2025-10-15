"""Structured logging configuration for SpaceCoreIskra.

Usage:
    from common.logging_config import get_logger
    
    logger = get_logger(__name__)
    logger.info("Processing request", extra={"facet": "Sam", "delta": 1})
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

_DEFAULT_LEVEL = "INFO"
_DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging with Iskra-specific fields."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON with canonical fields."""
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add Iskra-specific fields if present
        if hasattr(record, "facet"):
            log_data["facet"] = record.facet
        if hasattr(record, "delta"):
            log_data["∆"] = record.delta
        if hasattr(record, "omega"):
            log_data["Ω"] = record.omega
        if hasattr(record, "mirror"):
            log_data["mirror"] = record.mirror

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add any extra fields from extra parameter
        for key, value in record.__dict__.items():
            if key not in {
                "name",
                "msg",
                "args",
                "created",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "thread",
                "threadName",
                "exc_info",
                "exc_text",
                "stack_info",
                "facet",
                "delta",
                "omega",
                "mirror",
            }:
                log_data[key] = value

        return json.dumps(log_data, ensure_ascii=False)


def setup_logging(
    name: str,
    level: str | None = None,
    structured: bool = False,
    log_file: str | Path | None = None,
) -> logging.Logger:
    """Configure and return a logger instance.

    Parameters
    ----------
    name : str
        Logger name (typically __name__).
    level : str, optional
        Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        Defaults to INFO.
    structured : bool, default False
        If True, use JSON structured formatter.
    log_file : str | Path, optional
        If provided, also log to this file.

    Returns
    -------
    logging.Logger
        Configured logger instance.

    Examples
    --------
    >>> logger = setup_logging(__name__)
    >>> logger.info("Processing started")
    
    >>> logger = setup_logging(__name__, structured=True)
    >>> logger.info("Journal validated", extra={"shadow_ratio": 1.0})
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, (level or _DEFAULT_LEVEL).upper()))

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if structured:
        console_handler.setFormatter(StructuredFormatter())
    else:
        console_handler.setFormatter(
            logging.Formatter(
                _DEFAULT_FORMAT,
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
    logger.addHandler(console_handler)

    # File handler if requested
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(StructuredFormatter())
        logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(name: str, **kwargs: Any) -> logging.Logger:
    """Convenience wrapper around setup_logging.

    Parameters
    ----------
    name : str
        Logger name.
    **kwargs
        Additional arguments passed to setup_logging.

    Returns
    -------
    logging.Logger
        Configured logger.
    """
    return setup_logging(name, **kwargs)


# Example usage and smoke test
if __name__ == "__main__":  # pragma: no cover
    # Standard logging
    logger1 = get_logger("iskra.test")
    logger1.info("Standard format test")

    # Structured logging
    logger2 = get_logger("iskra.structured", structured=True)
    logger2.info(
        "Structured format test",
        extra={
            "facet": "Лиора",
            "delta": 1,
            "omega": 2,
            "mirror": "shadow-001",
        },
    )

    # With exception
    try:
        raise ValueError("Test exception")
    except ValueError:
        logger2.error("Error occurred", exc_info=True)

    print("\n✅ Logging configuration smoke test passed.")
