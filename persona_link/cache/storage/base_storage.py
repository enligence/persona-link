from abc import ABC, abstractmethod
from typing import AsyncGenerator, Optional
from persona_link.cache.models import ContentType

    
class BaseCacheStorage(ABC):
    """
    Base class for storage of video/audio files. Storage can be file system, 
    cloud storage, etc. The storage will store files in avatarId/file format.
    This way it will be possible to delete all files for a given persona_link.
    """
    
    @abstractmethod
    async def get(self, path: str) -> Optional[str]:
        """
        Get the url for the given path
        
        Parameters:
            path (str): The path of the file in the storage
        """
        pass

    @abstractmethod
    async def put(self, avatarId: str, data: bytes | AsyncGenerator[bytes, None], filename: str, content_type: ContentType) -> str:
        """
        Put the file in the avatarId folder and return the path
        
        Parameters:
            avatarId (str): The avatar ID
            data (bytes | AsyncGenerator[bytes, None]): The data to store
            filename (str): The filename of the file
            content_type (ContentType): The content type of the file
        """
        pass

    @abstractmethod
    async def delete(self, path: str) -> None:
        """
        Delete the data from the given path
        
        Parameters:
            path (str): The path of the file in the storage
        """
        pass

    @abstractmethod
    async def deleteAll(self, avatarId: str) -> None:
        """
        Delete all the data for the given avatar
        
        Parameters:
            avatarId (str): The avatar ID
        """
        pass