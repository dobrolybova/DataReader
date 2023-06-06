import os
from logging import getLogger

import aiofiles
from config import AppSettings

settings = AppSettings()

logger = getLogger(__name__)


class FileStorage:
    def __init__(self):
        self.storage_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../" + settings.FILE_NAME + ".json")

    async def write(self, data: dict[str, str]) -> None:
        async with aiofiles.open(self.storage_file, mode='a') as fp:
            await fp.write(str(data) + "\n")

    async def read_file(self) -> str:
        async with aiofiles.open(self.storage_file, mode='r') as fp:
            return await fp.read()

    async def read(self, _limit: int, _offset: int) -> list:
        data = await self.read_file()
        data = data.replace("'", "\"")
        data_list = data.split("\n")
        data_list.remove("")
        return data_list
