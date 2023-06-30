import json

from fastapi import APIRouter
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination import bases, paginate

from interface import StorageInterface
from schema import MessageSchema, MessagesOut


class Router(APIRouter):

    async def get_messages_from_db(self, limit: int = 10, offset: int = 0) -> list[MessagesOut]:
        return await self.storage.read(limit, offset)

    async def get_messages_from_file(self) -> bases.AbstractPage:
        messages_list = [json.loads(elem) for elem in await self.storage.read(0, 0)]
        messages_schemas = [MessageSchema(**elem) for elem in messages_list]
        return paginate(messages_schemas)

    def __init__(self, storage: StorageInterface):
        super().__init__()
        self.storage = storage
        self.add_api_route("/messages_db", self.get_messages_from_db, methods=["GET"],
                           response_model=list[MessagesOut])
        self.add_api_route("/messages_file", self.get_messages_from_file, methods=["GET"],
                           response_model=LimitOffsetPage[MessageSchema])
