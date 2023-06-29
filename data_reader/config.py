from enum import Enum

from pydantic import BaseSettings


class Storage(Enum):
    DB = 1,
    FILE = 2


DATABASE = {
    'drivername': 'postgresql+asyncpg',
    'host': 'localhost',
    'port': '5432',
    'username': 'yulia',
    'password': 'yulia',
    'database': 'messages',
    'query': {}
}


class AppSettings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = ""
    LOG_FORMAT: str = '%(asctime)s,%(levelname)-5s %(filename)s:%(funcName)s:%(lineno)-5d %(message)s'

    STORAGE: str = Storage.DB.name

    FILE_NAME: str = "data"
