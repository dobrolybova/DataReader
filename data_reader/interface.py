from typing import Protocol


class StorageInterface(Protocol):
    async def read(self, limit: int, offset: int) -> list:
        ...

    async def write(self, data: dict[str, str]) -> None:
        ...
