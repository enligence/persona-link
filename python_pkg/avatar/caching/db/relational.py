import asyncio
from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist
from avatar.caching.base.models import Record
from avatar.caching.base.base_db import BaseCacheDB
from avatar.caching.base.models import DBRecord
import os
from typing import Optional

class RelationalDB(BaseCacheDB):

    def __init__(self):
        self.DB_URL = os.getenv("DB_URL")
        if self.DB_URL is None:
            raise ValueError("DB_URL must be set in ENV")
        
        self.init_future = asyncio.ensure_future(self.init_db())
    
    async def init_db(self):
        await Tortoise.init(
            db_url=self.DB_URL,
            modules={'models': ['models']}
        )
        await Tortoise.generate_schemas()

    async def get(self, key: str) -> Optional[Record]:
        try:
            record = await DBRecord.get(key=key)
            return Record.from_db(record.dict())
        except DoesNotExist:
            return None

    async def put(self, record: Record) -> None:
        record_dict = record.model_dump()
        record_dict["filetypes"] = ','.join(record_dict["filetypes"])
        db_record = DBRecord(**record_dict)
        await db_record.save()

    async def incrementUsage(self, key: str) -> None:
        record = await self.get(key)
        if record:
            record.timesUsed += 1
            await record.save()

    async def delete(self, key: str) -> None:
        record = await self.get(key)
        if record:
            await record.delete()

    async def deleteAll(self, avatarId: str) -> None:
        records = DBRecord.filter(avatarId=avatarId)
        await records.delete()