import logging
from logging.config import dictConfig
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

def setup_logging():
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"}
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "default", "level": "INFO"},
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "level": "DEBUG",
                "filename": str(LOG_FILE),
                "maxBytes": 10 * 1024 * 1024,
                "backupCount": 5,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "app": {"handlers": ["console", "file"], "level": "DEBUG", "propagate": False},
            "app.services.a2s_service": {"handlers": ["console", "file"], "level": "DEBUG", "propagate": False},
            "uvicorn": {"handlers": ["console"], "level": "INFO", "propagate": True},
            "uvicorn.error": {"handlers": ["console", "file"], "level": "ERROR", "propagate": False},
        },
        "root": {"handlers": ["console", "file"], "level": "INFO"},
    }
    dictConfig(LOGGING_CONFIG)
