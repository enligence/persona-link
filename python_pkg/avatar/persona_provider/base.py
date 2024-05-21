from abc import ABC, abstractmethod
from avatar.persona_provider.models import (
    SpeakingAvatarInstance,
    AudioProviderSettings,
    VideoProviderSettings,
    Urls,
    AvatarType
)
from avatar.caching.cache import Cache
from avatar.caching.models import (
    DataToStore,
    Record,
)

"""
Base class for persona provider
"""


class PersonaBase(ABC):
    @abstractmethod
    async def generate(
        self, text: str, settings: AudioProviderSettings | VideoProviderSettings
    ) -> DataToStore:
        pass

    async def speak(
        self,
        cache: Cache,
        avatar_id: str,
        text: str,
        settings: AudioProviderSettings | VideoProviderSettings,
        isPersonalization: bool = False,
    ) -> SpeakingAvatarInstance:
        record: Record = await cache.get(avatar_id, text)
        
        avatar_type: AvatarType = (
            AvatarType.AUDIO
            if isinstance(settings, AudioProviderSettings)
            else AvatarType.VIDEO
        )
        
        if record is None:
            data: DataToStore = await self.generate(text, settings)
            record = await cache.put(avatar_id, text, data, isPersonalization)
            urls: Urls = await cache.get_urls(record)

            instance = SpeakingAvatarInstance(
                avatar_type=avatar_type, urls=urls, metadata=data.metadata
            )
        else:
            instance = SpeakingAvatarInstance(
                avatar_type=avatar_type,
                urls=await cache.get_urls(record),
                metadata=record.metadata,
            )
            
        await cache.incrementUsage(record.key)
        
        return instance
        
        
