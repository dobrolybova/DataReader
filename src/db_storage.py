import asyncio
from logging import getLogger
from typing import AsyncIterator

from config import DATABASE
from sqlalchemy import Column, Text, Integer, select
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = getLogger(__name__)
base = declarative_base()


class Messages(base):
    __tablename__ = 'messages'

    id = Column(Integer(), primary_key=True)
    component = Column(Text())
    country = Column(Text())
    description = Column(Text())
    model = Column(Text())


class DbStorage:
    def __init__(self):
        self.engine = create_async_engine(URL(**DATABASE), future=True, echo=True)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession)

    async def read(self, limit: int, offset: int) -> list:
        return [mes for mes in await self.async_session().scalars(select(Messages).limit(limit).offset(offset))]

    async def write(self, data: dict[str, str]) -> None:
        logger.debug(f"write message to DB {data}")
        async with self.async_session() as session:
            async with session.begin():
                session.add(Messages(**data))
                await session.commit()
