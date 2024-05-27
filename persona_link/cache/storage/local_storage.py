"""
Local storage for cache
"""
import shutil
import asyncio
import os
from typing import AsyncGenerator
import aiofiles
import aiofiles.os
from persona_link.cache.storage.base_storage import BaseCacheStorage
from persona_link.cache.models import ContentType

class LocalStorage(BaseCacheStorage):
    """
    Local storage for cache
    Requires ENV vars to be set for the path to the storage
    """

    def __init__(self):
        self.path = os.getenv("LOCAL_STORAGE_PATH")

        if self.path is None:
            raise ValueError("LOCAL_STORAGE_PATH must be set in ENV")

    async def put(self, avatarId: str, data: bytes | AsyncGenerator[bytes, None], filename: str, content_type: ContentType) -> str:
        """
        Put the data in the storage
        
        Parameters:
            avatarId (str): The avatar ID
            data (bytes): The data to be stored
            filename (str): The name of the file
            content_type (ContentType): The content type of the data
        """
        path = os.path.join(self.path, avatarId, filename)
        
        folder = os.path.dirname(path)
  
        # check if directory exists
        if not os.path.exists(folder): 
            # if the directory doesn't exists, create it
            os.makedirs(folder)
            
        async with aiofiles.open(path, "wb") as f:
            if isinstance(data, AsyncGenerator):
                async for chunk in data:
                    await f.write(chunk)
            else:
                await f.write(data)
        return path

    async def get(self, path: str) -> str:
        """
        Get the data from the storage
        
        Parameters:
            path (str): The path to the file in the storage
        """
        full_path = os.path.join(self.path, path)
        if os.path.exists(full_path):
            return full_path
        return None

    async def delete(self, path: str) -> None:
        """
        Delete the file from the storage
        
        Parameters:
            path (str): The path to the file in the storage
        """
        full_path = os.path.join(self.path, path)
        if await aiofiles.os.path.exists(full_path):
            await aiofiles.os.remove(full_path)

    async def deleteAll(self, avatarId: str) -> None:
        """
        Delete all the files for the given avatar
        
        Parameters:
            avatarId (str): The avatar ID
        """
        directory = os.path.join(self.path, avatarId)
        if os.path.exists(directory):
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, shutil.rmtree, directory)