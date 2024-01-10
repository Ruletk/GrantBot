"""Settings file for bot"""
import logging.config
import os

# Token for bot
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Database url
DATABASE_URL = os.environ.get("DATABASE_URL")

# Redis
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

# Logging settings
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
        "error_file_handler": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "logs/errors.log",
            "level": "WARNING",
        },
    },
    "loggers": {
        "aiogram": {
            "handlers": ["console", "error_file_handler"],
            "level": logging.DEBUG,
        },
        "sqlalchemy": {
            "handlers": ["console", "error_file_handler"],
            "level": logging.DEBUG,
        },
        "asyncpg": {
            "handlers": ["console", "error_file_handler"],
            "level": logging.DEBUG,
        },
        "src": {
            "handlers": ["console", "file_handler"],
            "level": logging.DEBUG,
        },
    },
}

logging.config.dictConfig(LOG_SETTINGS)
