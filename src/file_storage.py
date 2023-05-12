import os
from logging import getLogger

import aiofiles
from config import FILE_NAME

logger = getLogger(__name__)


class FileStorage:
    def __init__(self):
        self.storage_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../" + FILE_NAME + ".json")

    async def write(self, data: dict[str, str]) -> None:
        async with aiofiles.open(self.storage_file, mode='a') as fp:
            await fp.write(str(data) + "\n")

    async def read(self, _limit: int, _offset: int) -> list:
        async with aiofiles.open(self.storage_file, mode='r') as fp:
            data = await fp.read()
            data = data.replace("'", "\"")
        data_list = data.split("\n")
        data_list.remove("")
        return data_list
