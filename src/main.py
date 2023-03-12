import asyncio
import json
from logging import getLogger, basicConfig
from typing import List

import uvicorn
import websockets
from config import LOG_LEVEL, LOG_FILE, LOG_FORMAT
from db_storage import write
from fastapi import FastAPI
from fastapi_pagination import Page, add_pagination, paginate, LimitOffsetPage, bases
# from file_storage import write, read
from file_storage import read
from schema import MessageSchema, is_schema_matched

logger = getLogger(__name__)
basicConfig(filename=LOG_FILE, filemode='w', level=LOG_LEVEL, format=LOG_FORMAT)

WS_TASK = None


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
                logger.debug(f"{js}")
                write(js)
            else:
                logger.error(f"Not valid data: {js}")

            await asyncio.sleep(0.1)


async def startup() -> None:
    global WS_TASK
    WS_TASK = asyncio.create_task(ws_client())


async def shutdown() -> None:
    WS_TASK.cancel()

app = FastAPI(
    on_startup=[startup, ],
    on_shutdown=[shutdown, ]
)


@app.get('/messages', response_model=LimitOffsetPage[MessageSchema])
async def get_messages() -> bases.AbstractPage:
    messages_list = [json.loads(elem) for elem in read()]
    messages_schemas = [MessageSchema(**elem) for elem in messages_list]
    return paginate(messages_schemas)


add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app)
