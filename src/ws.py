import asyncio
import json
from json import JSONDecodeError
from logging import getLogger
from typing import Protocol

import websockets

from file_storage import FileStorage
from db_storage import DbStorage
from schema import is_schema_matched
from config import Storage, STORAGE

logger = getLogger(__name__)


class StorageInterface(Protocol):
    async def read(self, limit: int, offset: int) -> list:
        ...

    async def write(self, data: dict[str, str]) -> None:
        ...


storage_map = {Storage.DB: DbStorage, Storage.FILE: FileStorage}
storage: StorageInterface = storage_map[STORAGE]()


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
                await storage.write(js)
            else:
                logger.error(f"Not valid data: {js}")

            await asyncio.sleep(0.1)
