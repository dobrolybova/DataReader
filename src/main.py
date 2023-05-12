import asyncio
import json
from logging import getLogger, basicConfig

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination, LimitOffsetPage, bases, paginate

from config import LOG_LEVEL, LOG_FILE, LOG_FORMAT
from schema import MessageSchema, MessagesOut
from ws import ws_client, storage

logger = getLogger(__name__)
basicConfig(filename=LOG_FILE, filemode='w', level=LOG_LEVEL, format=LOG_FORMAT)

WS_TASK = None


async def startup() -> None:
    global WS_TASK
    WS_TASK = asyncio.create_task(ws_client())


async def shutdown() -> None:
    WS_TASK.cancel()


app = FastAPI(
    on_startup=[startup, ],
    on_shutdown=[shutdown, ]
)


@app.get('/messages_db', response_model=list[MessagesOut])
async def get_messages(limit: int = 10, offset: int = 0) -> list:
    return await storage.read(limit, offset)


@app.get('/messages_file', response_model=LimitOffsetPage[MessageSchema])
async def get_messages() -> bases.AbstractPage:
    messages_list = [json.loads(elem) for elem in await storage.read(0, 0)]
    messages_schemas = [MessageSchema(**elem) for elem in messages_list]
    return paginate(messages_schemas)


add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app)
