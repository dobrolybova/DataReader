import asyncio
import json
from logging import getLogger, basicConfig
from typing import List, AsyncIterator

import uvicorn
import websockets
from config import LOG_LEVEL, LOG_FILE, LOG_FORMAT
from config import async_session
from config import engine, Base
from db_storage import write, Messages
from fastapi import FastAPI, Depends
from fastapi_pagination import Page, add_pagination, LimitOffsetPage, bases, pagination_ctx, paginate
from fastapi_sqla import Base, Page, AsyncPaginate
# from file_storage import write, read
from file_storage import read
from pydantic import BaseModel
from schema import MessageSchema, is_schema_matched, MessagesOut
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select

logger = getLogger(__name__)
basicConfig(filename=LOG_FILE, filemode='w', level=LOG_LEVEL, format=LOG_FORMAT)

WS_TASK = None
DB_TASK = None


async def ws_client() -> None:
    async with websockets.connect('ws://localhost:8080') as websocket:
        while True:

            try:
                response = await websocket.recv()
            except websockets.ConnectionClosedOK:
                logger.critical(f"Connection closed OK")
            except websockets.ConnectionClosedError:
                logger.critical(f"Connection closed NOK")

            try:
                js = json.loads(response)
            except JSONDecodeError:
                logger.error(f"Received data is not json: {response}")
                continue

            if is_schema_matched(js):
                logger.info(f"{js}")
                await write(js)
            else:
                logger.error(f"Not valid data: {js}")

            await asyncio.sleep(0.1)


async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def startup() -> None:
    global WS_TASK, DB_TASK
    WS_TASK = asyncio.create_task(ws_client())
    DB_TASK = asyncio.create_task(start_db())


async def shutdown() -> None:
    WS_TASK.cancel()


app = FastAPI(
    on_startup=[startup, ],
    on_shutdown=[shutdown, ]
)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session


@app.get('/messages', response_model=list[MessagesOut])
async def get_messages(session: AsyncSession = Depends(get_db), limit: int = 10, offset: int = 0):
    return [mes for mes in await session.scalars(select(Messages).limit(limit).offset(offset))]


# @app.get('/messages', response_model=LimitOffsetPage[MessageSchema])
# async def get_messages() -> bases.AbstractPage:
#     messages_list = [json.loads(elem) for elem in read()]
#     messages_schemas = [MessageSchema(**elem) for elem in messages_list]
#     return paginate(messages_schemas)


add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app)
