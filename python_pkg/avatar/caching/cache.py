from base import BaseCacheStorage, BaseCacheDB
from typing import Any, Callable, Optional
from datetime import datetime

class Cache:
    """
    Class for caching of Avatar video / audio as per the 
    avatar type. Caching requires a blob storage for files, 
    database for metadata, and a hashing method to generate
    unique keys for the data.
    """
    def __init__(self, storage: BaseCacheStorage, db: BaseCacheDB, hashFn: Callable[[Any], str]):
        self.storage = storage
        self.db = db
        self.hashFn = hashFn

    def get(self, avatarId: str, text: str) -> Optional[str]:
        key = self.hashFn(avatarId + text)
        record = self.db.get(key)
        if record is None:
            return None
        self.db.incrementUsage(key)
        # get the url from storage
        return self.storage.getUrl(record.path)
    
    def put(self, avatarId: str, text: str, data: bytes, isPersonalization: bool = False) -> None:
        key = self.hashFn(avatarId + text)
        self.storage.put(path, data)
        record = Record(id=path, avatarId=avatarId, text=text, path=path, created=datetime.now(), isPersonalization=isPersonalization)
        self.db.put(record)

    def delete(self, key: str) -> None:
        self.storage.delete(key)
        self.db.delete(key)

    def deleteAll(self, avatarId: str) -> None:
        self.storage.deleteAll(avatarId)
        self.db.deleteAll(avatarId)
    
    def incrementUsage(self, key: str) -> None:
        self.db.incrementUsage(key)