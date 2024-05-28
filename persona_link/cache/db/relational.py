import os
from typing import Optional

from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist

from .base_db import BaseCacheDB
from .models import Record as DBRecord
from .models import UsageLog
from persona_link.cache.models import Record


class RelationalDB(BaseCacheDB):
    
    """
    Relational DB implementation of the BaseCacheDB. Should work with most Relation DB that [Tortoise ORM](https://tortoise.github.io/) supports.
    """

    def __init__(self):
        self.DB_URL = os.getenv("DB_URL", None)
        if not self.DB_URL:
            raise ValueError("DB_URL must be set in ENV")
    
    async def init_db(self):
        await Tortoise.init(
            db_url=self.DB_URL,
            modules={'models': ['persona_link.caching.db.models']}
        )
        await Tortoise.generate_schemas()

    async def get(self, key: str) -> Optional[Record]:
        """
        Get the record for the given key
        
        Parameters:
            key (str): The key for the record
        """
        try:
            record: DBRecord = await DBRecord.get(key=key)
            return Record.model_validate(record.__dict__)
        except DoesNotExist:
            return None

    async def put(self, record: Record) -> None:
        """
        Put the record in the database
        
        Parameters:
            record (Record): The record to put in the database
        """
        record_dict = record.model_dump()
        
        if record.storage_paths:
            record_dict['storage_paths'] = record.storage_paths.model_dump()
        if record.metadata:
            record_dict['metadata'] = record.metadata.model_dump()
            
        await DBRecord.create(**record_dict)

    async def incrementUsage(self, key: str) -> None:
        """
        Increment the usage count of the record for the given key
        
        Parameters:
            key (str): The key for the record
        """
        record: DBRecord = await DBRecord.get_or_none(key=key)
        if not record:
            print(f"No record found with key {key}")
        await UsageLog.create(record=record)
        
    async def getUsageCount(self, key: str) -> int:
        """
        Get the usage count of the record for the given key
        
        Parameters:
            key (str): The key for the record
        """
        record = await DBRecord.get_or_none(key=key)
        if record is None:
            return 0
        return await UsageLog.filter(record=record).count()

    async def delete(self, key: str) -> None:
        """
        Delete the record for the given key
        
        Parameters:
            key (str): The key for the record
        """
        record = await DBRecord.get_or_none(key=key)
        if record:
            await record.delete()

    async def deleteAll(self, avatarId: str) -> None:
        """
        Delete all the records for the given avatar
        
        Parameters:
            avatarId (str): The avatar ID
        """
        records = DBRecord.filter(avatarId=avatarId)
        await records.delete()