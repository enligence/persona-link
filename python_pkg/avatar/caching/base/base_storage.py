from abc import ABC, abstractmethod
from typing import AsyncGenerator, Optional

from python_pkg.avatar.caching.base.models import Record

class BaseCacheStorage(ABC):
    """
    Base class for storage of video/audio files. Storage can be file system, 
    cloud storage, etc. The storage will store files in avatarId/file format.
    This way it will be possible to delete all files for a given avatar.
    """

    @abstractmethod
    async def put(self, avatarId: str, data: bytes | AsyncGenerator[bytes, None], filename: str) -> str:
        """
        Put the file in the avatarId folder and return the path
        """
        pass

    @abstractmethod
    async def get(self, path: str) -> bytes:
        """
        Get the data from the given path
        """
        pass

    @abstractmethod
    async def delete(self, path: str) -> None:
        """
        Delete the data from the given path
        """
        pass

    @abstractmethod
    async def deleteAll(self, avatarId: str) -> None:
        """
        Delete all the data for the given avatar
        """
        pass
    """
    Base class for database to store metadata of the cached files
    """

    @abstractmethod
    async def get(self, key: str) -> Optional[Record]:
        """
        Get the record for the given key
        """
        pass

    @abstractmethod
    async def put(self, record: Record) -> None:
        """
        Put the record in the database
        """
        pass

    @abstractmethod
    async def incrementUsage(self, key: str) -> None:
        """
        Increment the usage count of the record for the given key
        """
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """
        Delete the record for the given key
        """
        pass

    @abstractmethod
    async def deleteAll(self, avatarId: str) -> None:
        """
        Delete all the records for the given avatar
        """
        pass