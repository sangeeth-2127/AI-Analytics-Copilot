"""
Logging Configuration

Central logging configuration for the
AI Analytics Copilot.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import logging
import logging.config
from pathlib import Path

from app.core.settings import settings

# =====================================================
# Log Directory
# =====================================================

LOG_DIR = Path(settings.LOG_DIR)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE = LOG_DIR / "application.log"


# =====================================================
# Logging Configuration
# =====================================================

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {

        "standard": {

            "format": (
                "%(asctime)s | "
                "%(levelname)-8s | "
                "%(name)s | "
                "%(message)s"
            ),

            "datefmt": "%Y-%m-%d %H:%M:%S",
        },

    },

    "handlers": {

        "console": {

            "class": "logging.StreamHandler",

            "formatter": "standard",

            "level": settings.LOG_LEVEL,
        },

        "file": {

            "class": "logging.handlers.RotatingFileHandler",

            "filename": str(LOG_FILE),

            "maxBytes": 10 * 1024 * 1024,

            "backupCount": 5,

            "encoding": "utf-8",

            "formatter": "standard",

            "level": settings.LOG_LEVEL,
        },

    },

    "root": {

        "handlers": [

            "console",

            "file",

        ],

        "level": settings.LOG_LEVEL,
    },

}


# =====================================================
# Public API
# =====================================================

_configured = False


def configure_logging() -> None:
    """
    Configure application logging.

    Safe to call multiple times.
    """

    global _configured

    if _configured:
        return

    logging.config.dictConfig(
        LOGGING_CONFIG
    )

    logger = logging.getLogger(__name__)

    logger.info("=" * 60)
    logger.info("Logging initialized")
    logger.info("Log Level : %s", settings.LOG_LEVEL)
    logger.info("Log File  : %s", LOG_FILE)
    logger.info("=" * 60)

    _configured = True