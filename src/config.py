import os

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from enum import Enum


class Storage(Enum):
    DB = 1,
    FILE = 2


# LOGGING
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "")
LOG_FORMAT = os.getenv("LOG_FORMAT", '%(asctime)s,%(levelname)-5s %(filename)s:%(funcName)s:%(lineno)-5d %(message)s')

# STORAGE
STORAGE = os.getenv("LOG_LEVEL", Storage.DB)

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

engine = create_async_engine(URL(**DATABASE), future=True, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession)
Base = declarative_base()
