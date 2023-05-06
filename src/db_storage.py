from logging import getLogger
from typing import AsyncIterator

from sqlalchemy import Column, Text, Integer
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE

logger = getLogger(__name__)

engine = create_async_engine(URL(**DATABASE), future=True, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession)
Base = declarative_base()


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer(), primary_key=True)
    component = Column(Text())
    country = Column(Text())
    description = Column(Text())
    model = Column(Text())


async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session


async def write(data: dict[str, str]) -> None:
    logger.debug(f"write message to DB {data}")
    async with async_session() as session:
        async with session.begin():
            session.add(Messages(**data))
            await session.commit()
