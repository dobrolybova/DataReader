import json
from json.decoder import JSONDecodeError
from logging import getLogger
from typing import Optional

from pydantic import BaseModel
from pydantic import ValidationError

logger = getLogger(__name__)


class MessageSchema(BaseModel):
    component: str
    country: str = "USA"
    description: str
    model: str


class MessagesOut(MessageSchema):
    id: int

    class Config:
        orm_mode = True

def is_schema_matched(data: dict[str, str]) -> bool:
    try:
        MessageSchema(**data)
    except TypeError as error:
        logger.error(f"{error}")
        return False
    except ValidationError as error:
        logger.error(f"{error}")
        return False
    return True
