"""
Local storage for cache
"""

import os
from typing import AsyncGenerator
import aiofiles
import aiofiles.os
from avatar.caching.base import BaseCacheStorage

class LocalStorage(BaseCacheStorage):
    """
    Local storage for cache
    Requires ENV vars to be set for the path to the storage
    """

    def __init__(self):
        self.path = os.getenv("LOCAL_STORAGE_PATH")

        if self.path is None:
            raise ValueError("LOCAL_STORAGE_PATH must be set in ENV")

    async def put(self, avatarId: str, data: bytes | AsyncGenerator[bytes, None], key: str, extension: str) -> None:
        path = os.path.join(self.path, avatarId, f"{key}.{extension}")
        async with aiofiles.open(path, "wb") as f:
            if isinstance(data, AsyncGenerator):
                async for chunk in data:
                    await f.write(chunk)
            else:
                await f.write(data)

    async def get(self, path: str) -> str:
        full_path = os.path.join(self.directory, path)
        if os.path.exists(full_path):
            return full_path
        return None

    async def delete(self, path: str) -> None:
        full_path = os.path.join(self.directory, path)
        if await aiofiles.os.path.exists(full_path):
            await aiofiles.os.remove(full_path)

    async def deleteAll(self, avatarId: str) -> None:
        directory = os.path.join(self.directory, avatarId)
        if await aiofiles.os.path.exists(directory):
            await aiofiles.os.rmdir(directory)