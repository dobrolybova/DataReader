import asyncio
import json
from logging import getLogger, basicConfig
from typing import List

import uvicorn
import websockets
from config import LOG_LEVEL, LOG_FILE, LOG_FORMAT
from fastapi import FastAPI
from fastapi_pagination import Page, add_pagination, paginate, LimitOffsetPage
from file_storage import write, read
from validator import MessageSchema
from validator import is_message_valid

logger = getLogger(__name__)
basicConfig(filename=LOG_FILE, filemode='w', level=LOG_LEVEL, format=LOG_FORMAT)

WS_TASK = None


async def ws_client():
    async with websockets.connect('ws://localhost:8080') as websocket:
        while True:
            try:
                response = await websocket.recv()
            except websockets.ConnectionClosedOK:
                logger.critical(f"Connection closed OK")
            except websockets.ConnectionClosedError:
                logger.critical(f"Connection closed NOK")
            if is_message_valid(response):
                logger.debug(f"{response}")
                write(response)
            else:
                logger.info(f"Not valid data: {response}")
            await asyncio.sleep(0.1)


async def startup():
    global WS_TASK
    WS_TASK = asyncio.create_task(ws_client())


async def shutdown():
    WS_TASK.cancel()

app = FastAPI(
    on_startup=[startup, ],
    on_shutdown=[shutdown, ]
)


@app.get('/messages', response_model=LimitOffsetPage[MessageSchema])
async def get_messages():
    messages_list = [json.loads(elem) for elem in read()]
    messages_schemas = [MessageSchema(**elem) for elem in messages_list]
    return paginate(messages_schemas)


add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app)
