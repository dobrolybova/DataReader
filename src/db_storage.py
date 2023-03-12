import json
from logging import getLogger

from peewee import *

logger = getLogger(__name__)

db = PostgresqlDatabase('messages', user='yulia')


class BaseModel(Model):
    class Meta:
        database = db


class Messages(BaseModel):
    component = TextField()
    country = TextField()
    description = TextField()
    model = TextField()

    class Meta:
        table_name = 'messages'


def write(data: dict[str, str]) -> None:
    logger.debug(f"write message to DB {data}")
    try:
        Messages.create(**data)
    except IntegrityError:
        logger.error(f"Add not valid data to DB: {data}")
    except TypeError as ex:
        logger.error(f"{ex}")


if __name__ == "__main__":
    # db.create_tables([Messages])
    pass
