import pytest
from dotenv import load_dotenv

from persona_link.cache.cache import Cache
from persona_link.cache.db import RelationalDB
from persona_link.cache.hashing import md5hash
from persona_link.cache.models import ContentType, DataToStore, Record
from persona_link.cache.storage import AzureStorage, LocalStorage
from persona_link.persona_provider.models import AvatarType, Urls, Viseme

load_dotenv()

@pytest.mark.asyncio
async def test_cache_local(cache):
    local_storage = LocalStorage()
    sqlite_db = RelationalDB()
    
    cache = Cache(local_storage, sqlite_db, md5hash)
    data: DataToStore = DataToStore(
        binary_data=b"data",
        content_type=ContentType.MP3,
        data_type=AvatarType.AUDIO,
        visemes=[Viseme(offset=0, viseme=21)],
    )
    
    await local_storage.deleteAll("avatarId")
    await sqlite_db.deleteAll("avatarId")
    
    await cache.put("avatarId", "text", data)
    record: Record = await cache.get("avatarId", "text")

    assert record is not None
    assert record.avatarId == "avatarId"
    urls: Urls = await cache.get_urls(record)
    assert urls.media_url is not None
    assert urls.visemes_url is not None
    assert urls.word_timestamps_url is None
    await cache.delete(record.key)
    assert await cache.get("avatarId", "text") is None


@pytest.mark.asyncio
async def test_cache_azure(cache):
    azure_storage = AzureStorage()
    sqlite_db = RelationalDB()
   
    data: DataToStore = DataToStore(
        binary_data=b"data",
        content_type=ContentType.MP3,
        data_type=AvatarType.AUDIO,
        visemes=[Viseme(offset=0, viseme=21)],
    )
    
    # test azure storage
    await azure_storage.deleteAll("avatarId")
    await sqlite_db.deleteAll("avatarId")

    cache = Cache(azure_storage, sqlite_db, md5hash)
    await cache.put("avatarId", "text", data)
    record: Record = await cache.get("avatarId", "text")
    assert record is not None
    assert record.avatarId == "avatarId"
    urls: Urls = await cache.get_urls(record)
    assert urls.media_url is not None
    assert urls.visemes_url is not None
    assert urls.word_timestamps_url is None
    await cache.delete(record.key)
    assert await cache.get("avatarId", "text") == None
    await azure_storage.deleteAll("avatarId")
    await sqlite_db.deleteAll("avatarId")