import pytest
from dotenv import load_dotenv

from persona_link.avatar.models import Avatar, AvatarInput, AvatarPydantic
from persona_link.cache.cache import Cache
from persona_link.cache.db import RelationalDB
from persona_link.cache.hashing import md5hash
from persona_link.cache.storage import LocalStorage
from persona_link.persona_provider.models import (
    SpeakingAvatarInstance,
)
from persona_link.tts import AzureTTS, AzureTTSVoiceSettings
from persona_link.avatar import speak

load_dotenv()


@pytest.fixture
def cache():
    local_storage = LocalStorage()
    sqlite_db = RelationalDB()
    return Cache(local_storage, sqlite_db, md5hash)


@pytest.mark.asyncio
async def test_audio_avatar(cache):
    avatar = await Avatar.create_avatar(
        AvatarPydantic(
            name="Jenny",
            provider="Audio",
            settings={
                "provider_name": "azure",
                "name": "en-US-JennyNeural",
                "visemes": False,
                "word_timestamps": True,
                "streaming": False,
            },
        )
    )

    assert avatar is not None
    assert avatar.provider.name == "Audio"
    assert avatar.settings is not None
    assert avatar.settings["name"] == "en-US-JennyNeural"
    assert avatar.settings["visemes"] == False
    assert avatar.settings["word_timestamps"] == True
    assert avatar.settings["streaming"] == False

    result: SpeakingAvatarInstance = await speak(
        avatar.slug, cache, AvatarInput(text="Hello World. How are you?")
    )

    assert result is not None
    assert result.urls.media_url is not None
    assert result.urls.visemes_url is None
    assert result.urls.word_timestamps_url is not None
    assert result.metadata is not None
    assert result.metadata.duration_seconds > 0


@pytest.mark.asyncio
async def test_sprite_avatar(cache):
    avatar = await Avatar.create_avatar(
        AvatarPydantic(
            name="JennySprite",
            provider="Sprite",
            settings={
                "sprite_image_url": "abc",
                "eye_blink_url": "def",
                "audio_settings": {
                    "provider_name": "azure",
                    "name": "en-US-JennyNeural",
                    "visemes": False,
                    "word_timestamps": True,
                    "streaming": False,
                }
            },
        )
    )

    assert avatar is not None
    assert avatar.provider.name == "Sprite"
    assert avatar.settings is not None
    assert avatar.settings["sprite_image_url"] == "abc"
    assert avatar.settings["eye_blink_url"] == "def"
    assert avatar.settings["audio_settings"]["name"] == "en-US-JennyNeural"
    assert avatar.settings["audio_settings"]["visemes"] == False
    assert avatar.settings["audio_settings"]["word_timestamps"] == True
    assert avatar.settings["audio_settings"]["streaming"] == False

    result: SpeakingAvatarInstance = await speak(
        avatar.slug, cache, AvatarInput(text="Hello World")
    )

    assert result is not None
    assert result.urls.media_url is not None
    assert result.urls.visemes_url is None
    assert result.urls.word_timestamps_url is not None
    assert result.metadata is not None
    assert result.metadata.duration_seconds > 0


@pytest.mark.asyncio
async def test_azure_avatar(cache):
    avatar = await Avatar.create_avatar(
        AvatarPydantic(
            name="Lisa",
            provider="Azure",
            settings={
                "voice": "en-IN-NeerjaNeural",
                "character": "lisa",
                "style": "graceful",
                "pose": "sitting",
                "video_format": "mp4",
                "background_color": "#ffffff",
                "video_codec": "hevc",
            },
        )
    )

    assert avatar is not None
    assert avatar.provider.name == "Azure"
    assert avatar.settings is not None
    assert avatar.settings["voice"] == "en-IN-NeerjaNeural"
    assert avatar.settings["character"] == "lisa"
    assert avatar.settings["style"] == "graceful"
    assert avatar.settings["pose"] == "sitting"
    assert avatar.settings["video_format"] == "mp4"
    assert avatar.settings["background_color"] == "#ffffff"
    assert avatar.settings["video_codec"] == "hevc"

    result: SpeakingAvatarInstance = await speak(
        avatar.slug, cache, AvatarInput(text="Hello")
    )

    assert result is not None
    assert result.urls.media_url is not None
    assert result.urls.visemes_url is None
    assert result.urls.word_timestamps_url is None
    assert result.metadata is not None


@pytest.mark.asyncio
async def test_heygen_avatar(cache):
    avatar = await Avatar.create_avatar(
        AvatarPydantic(
            name="Karolin",
            provider="Heygen",
            settings={
                "heygen_id": "Karolin_public_20230109",
                "avatar_style": "normal",
                "voice_id": "131a436c47064f708210df6628ef8f32",
                "background_color": "#ffff00",
                "background_type": "color",
                "background_asset_id": None,
                "test": True,
            },
        )
    )

    assert avatar is not None
    assert avatar.provider.name == "Heygen"
    assert avatar.settings is not None
    assert avatar.settings["heygen_id"] == "Karolin_public_20230109"
    assert avatar.settings["avatar_style"] == "normal"
    assert avatar.settings["voice_id"] == "131a436c47064f708210df6628ef8f32"
    assert avatar.settings["background_color"] == "#ffff00"
    assert avatar.settings["background_type"] == "color"
    assert avatar.settings["background_asset_id"] == None
    assert avatar.settings["test"] == True

    result: SpeakingAvatarInstance = await speak(
        avatar.slug, cache, AvatarInput(text="Hello")
    )

    assert result is not None
    assert result.urls.media_url is not None
    assert result.urls.visemes_url is None
    assert result.urls.word_timestamps_url is None
    assert result.metadata is not None
