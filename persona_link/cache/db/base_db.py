from abc import ABC, abstractmethod
from typing import Optional

from persona_link.cache.models import Record


class BaseCacheDB(ABC):
    """
    Base class for database to store metadata of the cached files
    """

    @abstractmethod
    async def get(self, key: str) -> Optional[Record]:
        """
        Get the record for the given key
        
        Parameters:
            key (str): The key for the record
        """
        pass

    @abstractmethod
    async def put(self, record: Record) -> None:
        """
        Put the record in the database
        
        Parameters:
            record (Record): The record to put in the database
        """
        pass

    @abstractmethod
    async def incrementUsage(self, key: str) -> None:
        """
        Increment the usage count of the record for the given key
        
        Parameters:
            key (str): The key for the record
        """
        pass
    
    @abstractmethod
    async def getUsageCount(self, key: str) -> int:
        """
        Get the usage count of the record for the given key
         
        Parameters:
            key (str): The key for the record
        """
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        """
        Delete the record for the given key
        
        Parameters:
            key (str): The key for the record
        """
        pass

    @abstractmethod
    async def deleteAll(self, avatarId: str) -> None:
        """
        Delete all the records for the given avatar
        
        Parameters:
            avatarId (str): The avatar ID
        """
        pass