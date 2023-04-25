import asyncio
import json
from logging import getLogger

import websockets
from db_storage import write
from file_storage import read
from schema import is_schema_matched
# from file_storage import write, read

logger = getLogger(__name__)


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
