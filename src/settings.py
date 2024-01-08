"""Settings file for bot"""
import logging.config
import os

# Token for bot
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Database url
DATABASE_URL = os.environ.get("DATABASE_URL")

LOG_SETTINGS = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s  %(levelname)-8s  %(name)-30s  %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "logs/logs.log",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "aiogram": {
            "handlers": ["console"],
            "level": logging.DEBUG,
        },
        "sqlalchemy": {
            "handlers": ["console"],
            "level": logging.DEBUG,
        },
        "asyncpg": {
            "handlers": ["console"],
            "level": logging.DEBUG,
        },
        "src": {
            "handlers": ["console", "file_handler"],
            "level": logging.DEBUG,
        },
    },
}

logging.config.dictConfig(LOG_SETTINGS)
