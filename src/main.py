import asyncio
import json
from logging import getLogger, basicConfig

import uvicorn
from config import LOG_LEVEL, LOG_FILE, LOG_FORMAT
from db_storage import Messages, start_db, get_db
from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination, LimitOffsetPage, bases, paginate
from file_storage import read
from schema import MessageSchema, MessagesOut
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ws import ws_client

logger = getLogger(__name__)
basicConfig(filename=LOG_FILE, filemode='w', level=LOG_LEVEL, format=LOG_FORMAT)

WS_TASK = None
DB_TASK = None


async def startup() -> None:
    global WS_TASK, DB_TASK
    WS_TASK = asyncio.create_task(ws_client())
    DB_TASK = asyncio.create_task(start_db())


async def shutdown() -> None:
    WS_TASK.cancel()
    DB_TASK.cancel()


app = FastAPI(
    on_startup=[startup, ],
    on_shutdown=[shutdown, ]
)


@app.get('/messages', response_model=list[MessagesOut])
async def get_messages(session: AsyncSession = Depends(get_db), limit: int = 10, offset: int = 0) -> list:
    return [mes for mes in await session.scalars(select(Messages).limit(limit).offset(offset))]


# @app.get('/messages', response_model=LimitOffsetPage[MessageSchema])
# async def get_messages() -> bases.AbstractPage:
#     messages_list = [json.loads(elem) for elem in read()]
#     messages_schemas = [MessageSchema(**elem) for elem in messages_list]
#     return paginate(messages_schemas)


add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app)
