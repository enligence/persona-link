from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist
from avatar.caching.models import Record
from .base_db import BaseCacheDB
from avatar.caching.db.models import Record as DBRecord, UsageLog
import os
from typing import Optional

class RelationalDB(BaseCacheDB):

    def __init__(self):
        self.DB_URL = os.getenv("DB_URL", None)
        if not self.DB_URL:
            raise ValueError("DB_URL must be set in ENV")
    
    async def init_db(self):
        await Tortoise.init(
            db_url=self.DB_URL,
            modules={'models': ['avatar.caching.db.models']}
        )
        await Tortoise.generate_schemas()

    async def get(self, key: str) -> Optional[Record]:
        try:
            record: DBRecord = await DBRecord.get(key=key)
            return Record.model_validate(record.__dict__)
        except DoesNotExist:
            return None

    async def put(self, record: Record) -> None:
        record_dict = record.model_dump()
        
        if record.storage_paths:
            record_dict['storage_paths'] = record.storage_paths.model_dump()
        if record.metadata:
            record_dict['metadata'] = record.metadata.model_dump()
            
        await DBRecord.create(**record_dict)

    async def incrementUsage(self, key: str) -> None:
        record: DBRecord = await DBRecord.get_or_none(key=key)
        if not record:
            print(f"No record found with key {key}")
        await UsageLog.create(record=record)
        
    async def getUsageCount(self, key: str) -> int:
        record = await DBRecord.get_or_none(key=key)
        if record is None:
            return 0
        return await UsageLog.filter(record=record).count()

    async def delete(self, key: str) -> None:
        record = await DBRecord.get_or_none(key=key)
        if record:
            await record.delete()

    async def deleteAll(self, avatarId: str) -> None:
        records = DBRecord.filter(avatarId=avatarId)
        await records.delete()