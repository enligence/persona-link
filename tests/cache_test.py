import pytest
import os
from dotenv import load_dotenv
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "python_pkg"))
)

from avatar.caching.storages import LocalStorage, AzureStorage
from avatar.caching.db import RelationalDB
from avatar.caching.cache import Cache
from avatar.caching.models import (
    ContentType,
    DataToStore,
    Record
)
from avatar.caching.hashing import md5hash
from avatar.persona_provider.models import (
    Viseme, 
    AudioInstance,
    Urls,
    AvatarType,
    VideoFormat,
    VideoCodecs
)
from avatar.tts import AzureTTSVoiceSettings, AzureTTS

from avatar.persona_provider.sprite import SpriteAvatar
from avatar.persona_provider.heygen import HeygenAvatar, HeygenAvatarSettings
from avatar.persona_provider.azure import AzureAvatar, AzureAvatarSettings, AzureAvatarStyle, AzureAvatarPose

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
        data_type=AvatarType.AUDIO,
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
    
    #tts = AzureTTS()
    text = "This is a test with some background. And this is the fifth request for today sso the last one. I hope this works!"
    # audio: AudioInstance = await tts.synthesize_speech(text, settings=settings)
    # assert audio.content is not None and len(audio.content) > 0
    # assert audio.visemes is not None and len(audio.visemes) > 0
    # assert audio.word_timestamps is not None and len(audio.word_timestamps) > 0
    
    # data: DataToStore = DataToStore(
    #     binary_data=audio.content,
    #     content_type=ContentType.MP3,
    #     data_type=AvatarType.AUDIO,
    #     visemes=audio.visemes,
    #     word_timestamps=audio.word_timestamps
    # )
    
    # await cache.put("avatarId", text, data)
    # record: Record = await cache.get("avatarId", text)
    # assert record is not None
    # assert record.avatarId == "avatarId"
    # urls: Urls = await cache.get_urls(record)
    # print(urls)
    # assert urls.media_url is not None
    # assert urls.viseme_url is not None
    # assert urls.word_timestamp_url is not None
    # await cache.delete(record.key)
    # assert await cache.get("avatarId", text) == None
    
    # Now test the providers
    # savatar = SpriteAvatar()
    # speech = await savatar.speak(cache, "avatarId", text, settings)
    # assert speech is not None
    # assert speech.urls.media_url is not None
    # assert speech.urls.viseme_url is not None
    # assert speech.urls.word_timestamp_url is not None
    # assert speech.metadata is not None
    # assert speech.metadata.duration_seconds > 0
    # record: Record = await cache.get("avatarId", text)
    # assert record  is not None
    # await cache.delete(record.key)
    
    # test heygen
    # havatar = HeygenAvatar()
    # """
    # class HeygenAvatarSettings(VideoProviderSettings):
    # heygen_id: str
    # avatar_style: str
    # voice_id: str
    # background_color: Optional[str] = None
    # background_type: str = "color"
    # background_asset_id: Optional[str] = None
    # test: bool = True
    # api_token: str
    # """
    # heygen_settings = HeygenAvatarSettings(
    #     heygen_id="Karolin_public_20230109",
    #     avatar_style="normal",
    #     voice_id="131a436c47064f708210df6628ef8f32",
    #     background_color="#ffff00",
    #     background_type="color",
    #     background_asset_id=None,
    #     test=True,
    #     api_token=os.getenv("HEYGEN_API_TOKEN")
    # )
    
    # hspeech = await havatar.speak(cache, "karolin", text, heygen_settings)
    # assert hspeech is not None
    # assert hspeech.urls.media_url is not None
    
    # Test Azure Avatar
    """
    voice: str = "en-IN-NeerjaNeural"
    character: str = "lisa"
    style: AzureAvatarStyle = AzureAvatarStyle.GRACEFUL
    pose: AzureAvatarPose = AzureAvatarPose.SITTING
    video_format: VideoFormat = VideoFormat.WEBM
    background_color: str = "#00000000"
    video_codec = "vp9"""
    azure_avatar_settings = AzureAvatarSettings(
        voice="en-IN-NeerjaNeural",
        character="lisa",
        style=AzureAvatarStyle.GRACEFUL,
        pose=AzureAvatarPose.SITTING,
        video_format=VideoFormat.WEBM,
        background_color="#00000000",
        video_codec=VideoCodecs.VP9
    )
    
    azure_avatar = AzureAvatar()
    text = "Hi, I am Lisa. I am a graceful avatar. I am sitting. I am speaking in English. I hope you like my voice. Can I know more about you please?"
    aspeech = await azure_avatar.speak(cache, "lisa", text, azure_avatar_settings)
    
    assert aspeech is not None
    assert aspeech.urls.media_url is not None
        
    
    
    
    
    
