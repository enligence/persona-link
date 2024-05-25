from abc import ABC, abstractmethod
from persona_link.persona_provider.models import (
    SpeakingAvatarInstance,
    AudioProviderSettings,
    VideoProviderSettings,
    Urls,
    AvatarType
)
from persona_link.cache.cache import Cache
from persona_link.cache.models import (
    DataToStore,
    Record,
)

"""
Base class for persona provider
"""


class PersonaBase(ABC):
    @classmethod
    @abstractmethod
    def validate(cls, settings: dict) -> AudioProviderSettings | VideoProviderSettings | None:
        pass
    
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
        settings: AudioProviderSettings | VideoProviderSettings
    ) -> SpeakingAvatarInstance:
        record: Record = await cache.get(avatar_id, text)
        
        avatar_type: AvatarType = (
            AvatarType.AUDIO
            if isinstance(settings, AudioProviderSettings)
            else AvatarType.VIDEO
        )
        
        if record is None:
            data: DataToStore = await self.generate(text, settings)
            record = await cache.put(avatar_id, text, data)
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
        
        
