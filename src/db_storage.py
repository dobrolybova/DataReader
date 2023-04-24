from logging import getLogger

from config import Base, async_session
from sqlalchemy import Column, Text, Integer
from sqlalchemy.orm import sessionmaker

logger = getLogger(__name__)


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer(), primary_key=True)
    component = Column(Text())
    country = Column(Text())
    description = Column(Text())
    model = Column(Text())


async def write(data: dict[str, str]) -> None:
    logger.debug(f"write message to DB {data}")
    async with async_session() as session:
        async with session.begin():
            session.add(Messages(**data))
            session.commit()
