import pytest
import os
from dotenv import load_dotenv
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "python_pkg"))
)

from avatar.caching.storages.local_storage import LocalStorage
from avatar.caching.storages.azure_storage import AzureStorage
from avatar.caching.db.relational import RelationalDB
from avatar.caching.cache import Cache
from avatar.caching.base.models import (
    ContentType,
    DataToStore,
    DataType,
    Record,
    Urls,
)
from avatar.caching.hashing import md5hash
from avatar.tts.models import Viseme
from avatar.tts.azure_tts import AzureTTS, AzureTTSVoiceSettings
from avatar.tts.models import AudioInstance

load_dotenv()


print(sys.path)


@pytest.mark.asyncio
async def test_cache():
    local_storage = LocalStorage()
    azure_storage = AzureStorage()
    sqlite_db = RelationalDB()
    await sqlite_db.init_db()
    await local_storage.deleteAll("avatarId")
    await sqlite_db.deleteAll("avatarId")
    cache = Cache(local_storage, sqlite_db, md5hash)
    data: DataToStore = DataToStore(
        binary_data=b"data",
        content_type=ContentType.MP3,
        data_type=DataType.AUDIO,
        visemes=[Viseme(offset=0, viseme=21)],
    )
    await cache.put("avatarId", "text", data)
    record: Record = await cache.get("avatarId", "text")
    assert record is not None
    assert record.avatarId == "avatarId"
    urls: Urls = await cache.get_urls(record)
    assert urls.media_url is not None
    assert urls.viseme_url is not None
    assert urls.word_timestamp_url is None
    await cache.delete(record.key)
    assert await cache.get("avatarId", "text") == None
    
    # test azure storage
    #await azure_storage.deleteAll("avatarId")
    await local_storage.deleteAll("avatarId")
    await sqlite_db.deleteAll("avatarId")
    
    cache = Cache(azure_storage, sqlite_db, md5hash)
    await cache.put("avatarId", "text", data)
    record: Record = await cache.get("avatarId", "text")
    assert record is not None
    assert record.avatarId == "avatarId"
    urls: Urls = await cache.get_urls(record)
    print(urls)
    assert urls.media_url is not None
    assert urls.viseme_url is not None
    assert urls.word_timestamp_url is None
    await cache.delete(record.key)
    assert await cache.get("avatarId", "text") == None
    await azure_storage.deleteAll("avatarId")
    await sqlite_db.deleteAll("avatarId")
    
    # test azure TTS
    settings = AzureTTSVoiceSettings(
        subscription_key=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
        name="en-US-JennyNeural",
        visemes=True,
        word_timestamps=True,
        streaming=False
    )
    
    tts = AzureTTS()
    text = "This is a test."
    audio: AudioInstance = await tts.synthesize_speech(text, settings=settings)
    assert audio.content is not None and len(audio.content) > 0
    assert audio.visemes is not None and len(audio.visemes) > 0
    assert audio.word_timestamps is not None and len(audio.word_timestamps) > 0
    
    
    
    
