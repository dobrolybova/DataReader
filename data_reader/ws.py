import asyncio
import json
from json import JSONDecodeError
from logging import getLogger

import websockets

from interface import StorageInterface
from schema import is_schema_matched

logger = getLogger(__name__)


async def ws_client(storage: StorageInterface) -> None:
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
                await storage.write(js)
            else:
                logger.error(f"Not valid data: {js}")

            await asyncio.sleep(0.1)
