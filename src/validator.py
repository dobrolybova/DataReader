import json
from json.decoder import JSONDecodeError

from pydantic import BaseModel
from pydantic import ValidationError


class MessageSchema(BaseModel):
    component: str
    country: str = "USA"
    description: str
    model: str


def is_message_valid(data: json) -> bool:
    try:
        kwargs = json.loads(data)
    except JSONDecodeError:
        return False
    try:
        MessageSchema(**kwargs)
    except TypeError as _error:
        return False
    except ValidationError as _error:
        return False
    return True
