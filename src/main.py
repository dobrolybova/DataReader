import asyncio

import file_storage
import websockets
from validator import is_message_valid
from timed_rotating_text_file import TimedRotatingTextFile


async def main():
    async with websockets.connect('ws://localhost:8080') as websocket:
        while True:
            try:
                response = await websocket.recv()
            except websockets.ConnectionClosedOK:
                print(f"Connection closed OK")
            except websockets.ConnectionClosedError:
                print(f"Connection closed NOK")
            if is_message_valid(response):
                print(response)
                file_storage.write(response)
            else:
                print(f"Not valid data: {response}")
            await asyncio.sleep(1)


asyncio.run(main())
