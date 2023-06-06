import asyncio
from logging import getLogger, basicConfig

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from config import AppSettings, Storage
from db_storage import DbStorage
from file_storage import FileStorage
from interface import StorageInterface
from routers import Router
from ws import ws_client

settings = AppSettings()

logger = getLogger(__name__)
basicConfig(filename=settings.LOG_FILE, filemode='w', level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)

storage_map = {Storage.DB.name: DbStorage, Storage.FILE.name: FileStorage}


class Application:
    WS_TASK = None

    async def startup(self) -> None:
        self.ws_task = asyncio.create_task(ws_client(self.storage))

    async def shutdown(self) -> None:
        self.ws_task.cancel()

    def __init__(self, app_settings: AppSettings) -> None:
        self.storage: StorageInterface = storage_map[app_settings.STORAGE]()
        self.ws_task = None
        self.router = Router(self.storage)
        self.app = FastAPI(
            on_startup=[self.startup, ],
            on_shutdown=[self.shutdown, ]
        )
        self.app.include_router(self.router)
        add_pagination(self.app)


if __name__ == "__main__":
    uvicorn.run(Application(settings).app)
