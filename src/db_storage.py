from logging import getLogger
from typing import AsyncIterator

import psycopg2
from config import DATABASE, Base, async_session, engine, Base, async_session
from sqlalchemy import Column, Text, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

logger = getLogger(__name__)

sql_commands = (
        # """
        # CREATE USER yulia WITH SUPERUSER PASSWORD 'yulia'
        # """,
        """
        CREATE database messages
        """,
)


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer(), primary_key=True)
    component = Column(Text())
    country = Column(Text())
    description = Column(Text())
    model = Column(Text())


def create_db(commands: tuple[str]):
    conn = psycopg2.connect(database="postgres",
                            user=DATABASE["username"],
                            password=DATABASE["password"],
                            host=DATABASE["host"],
                            port=DATABASE["port"])
    conn.autocommit = True
    cursor = conn.cursor()
    for command in commands:
        cursor.execute(command)
    conn.commit()
    conn.close()


async def start_db():
    try:
        create_db(sql_commands)
    except psycopg2.errors.DuplicateDatabase:
        logger.debug(f"DB messages already exist")
        pass
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session


async def write(data: dict[str, str]) -> None:
    logger.debug(f"write message to DB {data}")
    async with async_session() as session:
        async with session.begin():
            session.add(Messages(**data))
            await session.commit()
