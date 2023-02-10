import asyncio

import file_storage
import websockets
from validator import is_message_valid
from timed_rotating_text_file import TimedRotatingTextFile
from logger import logger


async def main():
    async with websockets.connect('ws://localhost:8080') as websocket:
        while True:
            try:
                response = await websocket.recv()
            except websockets.ConnectionClosedOK:
                logger.critical(f"Connection closed OK")
            except websockets.ConnectionClosedError:
                logger.critical(f"Connection closed NOK")
            if is_message_valid(response):
                logger.info(f"{response}")
                file_storage.write(response)
            else:
                logger.info(f"Not valid data: {response}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
