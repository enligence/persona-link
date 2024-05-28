import json
from datetime import datetime
from typing import Any, Callable, Optional

from persona_link.cache.db import BaseCacheDB
from persona_link.cache.models import (EXTENSION_MAPPING, ContentType,
                                       DataToStore, Record, StoragePaths)
from persona_link.cache.storage import BaseCacheStorage
from persona_link.persona_provider.models import Urls


class Cache:
    """
    Class for caching of Avatar video / audio as per the
    avatar type. Caching requires a blob storage for files,
    database for metadata, and a hashing method to generate
    unique keys for the data.
    """

    def __init__(
        self, storage: BaseCacheStorage, db: BaseCacheDB, hashFn: Callable[[Any], str]
    ):
        """
        Constructor for Cache class.
        
        Parameters:
            storage (BaseCacheStorage): The storage for the cache
            db (BaseCacheDB): The database for the cache
            hashFn (Callable[[Any], str]): The hashing function to generate keys
        """
        if storage is None:
            raise ValueError("storage cannot be None")
        self.storage = storage
        if db is None:
            raise ValueError("db cannot be None")
        self.db = db
        if hashFn is None:
            raise ValueError("hashFn cannot be None")
        self.hashFn = hashFn

    async def get(self, avatarId: str, text: str) -> Optional[Record]:
        """
        Get the record from the cache
        
        Parameters:
            avatarId (str): The avatar ID
            text (str): The text to get the record for
            
        Returns:
            The record for the given avatar ID and text
        """
        key = self.hashFn(avatarId + text)
        record = await self.db.get(key)
        if record is None:
            return None
        return record
    
    async def get_urls(self, record: Record) -> Urls:
        """
        Get the URLs for the media, visemes, and word timestamps
        
        Parameters:
            record (Record): The record to get the URLs for
            
        Returns:
            The URLs for the media, visemes, and word timestamps
        """
        return Urls(
            media_url = await self.storage.get(record.storage_paths.media_path),
            viseme_url = await self.storage.get(record.storage_paths.viseme_path) if record.storage_paths.viseme_path else None,
            word_timestamp_url = await self.storage.get(record.storage_paths.word_timestamp_path) if record.storage_paths.word_timestamp_path else None,
        )
        
    async def getUsageCount(self, key: str) -> int:
        """
        Get the usage count of the record for the given key
        
        Parameters:
            key (str): The key for the record
            
        Returns:
            The usage count for the given key
        """
        return await self.db.getUsageCount(key)

    async def put(
        self,
        avatarId: str,
        text: str,
        data: DataToStore,
    ) -> Record:
        """
        Put the record in the cache
        
        Parameters:
            avatarId (str): The avatar ID
            text (str): The text to put the record for
            data (DataToStore): The data to store in the cache
            
        Returns:
            The record that was put in the cache
        """
        key = self.hashFn(avatarId + text)
        media_path = await self.storage.put(
            avatarId,
            data.binary_data,
            f"{key}{EXTENSION_MAPPING[data.content_type]}",
            data.content_type,
        )
        visemes_path = None
        word_timestamps_path = None
        if data.visemes is not None:
            viseme_bytes = json.dumps([v.model_dump() for v in data.visemes]).encode(
                "utf-8"
            )  # Convert Viseme instances to dict, then to JSON string, then to bytes
            visemes_path = await self.storage.put(
                avatarId, viseme_bytes, f"{key}-visemes.json", ContentType.JSON
            )

        if data.word_timestamps is not None:
            word_timestamps_bytes = json.dumps(
                [w.model_dump() for w in data.word_timestamps]
            ).encode("utf-8")
            word_timestamps_path = await self.storage.put(
                avatarId,
                word_timestamps_bytes,
                f"{key}-word-timestamps.json",
                ContentType.JSON,
            )

        record = Record(
            key=key,
            avatarId=avatarId,
            text=text,
            created=datetime.now(),
            metadata=data.metadata,
            storage_paths=StoragePaths(
                media_path=media_path,
                viseme_path=visemes_path,
                word_timestamp_path=word_timestamps_path,
            ),
        )

        await self.db.put(record)
        
        return record

    async def delete(self, key: str) -> None:
        """
        Delete the record for the given key
        
        Parameters:
            key (str): The key for the record
        """
        record: Record = await self.db.get(key)
        if record is None:
            return
        await self.storage.delete(record.storage_paths.media_path)
        if record.storage_paths.viseme_path:
            await self.storage.delete(record.storage_paths.viseme_path)
        if record.storage_paths.word_timestamp_path:
            await self.storage.delete(record.storage_paths.word_timestamp_path)
        await self.db.delete(key)

    async def deleteAll(self, avatarId: str) -> None:
        """
        Delete all the records for the given avatar
        
        Parameters:
            avatarId (str): The avatar ID
        """
        await self.storage.deleteAll(avatarId)
        await self.db.deleteAll(avatarId)

    async def incrementUsage(self, key: str) -> None:
        """
        Increment the usage count of the record for the given key
        
        Parameters:
            key (str): The key for the record
        """
        await self.db.incrementUsage(key)
