import os

from enum import Enum


class Storage(Enum):
    DB = 1,
    FILE = 2


# LOGGING
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "")
LOG_FORMAT = os.getenv("LOG_FORMAT", '%(asctime)s,%(levelname)-5s %(filename)s:%(funcName)s:%(lineno)-5d %(message)s')

# STORAGE
STORAGE = os.getenv("STORAGE", Storage.FILE)

# FILE
FILE_NAME = os.getenv("FILE_NAME", "data")

# DB
DATABASE = {
    'drivername': 'postgresql+asyncpg',
    'host': 'localhost',
    'port': '5432',
    'username': 'yulia',
    'password': 'yulia',
    'database': 'messages',
    'query': {}
}
