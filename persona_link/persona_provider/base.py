from abc import ABC, abstractmethod

from persona_link.cache.cache import Cache
from persona_link.cache.models import DataToStore, Record
from .models import (
    AudioProviderSettings,
    AvatarType,
    SpeakingAvatarInstance,
    Urls,
    VideoProviderSettings,
)


class PersonaBase(ABC):
    """
    Base class for persona provider. A persona provider is the one responsible to take some text and settings
    and generate the corresponding audio or video.
    """

    @classmethod
    @abstractmethod
    def validate(
        cls, settings: dict
    ) -> AudioProviderSettings | VideoProviderSettings | None:
        """
        Validate the settings for the provider. This method should return the settings object if the settings are valid

        Parameters:
            settings (dict): The settings for the provider

        Returns:
            settings of respective provider if the settings are valid otherwise None
        """
        pass

    @abstractmethod
    async def generate(
        self, text: str, settings: AudioProviderSettings | VideoProviderSettings
    ) -> DataToStore:
        """
        Generate the audio or video for the avatar

        Parameters:
            text (str): The text to be spoken by the avatar
            settings (AudioProviderSettings | VideoProviderSettings): The settings for the provider

        Returns:
            The data to store for the audio or video along with other metadata
        """
        pass

    async def speak(
        self,
        cache: Cache,
        avatar_id: str,
        text: str,
        settings: AudioProviderSettings | VideoProviderSettings,
    ) -> SpeakingAvatarInstance:
        """
        Speak the input text using the avatar with the given slug

        Parameters:
            cache (Cache): The cache object to use
            avatar_id (str): The avatar ID
            text (str): The input text to speak
            settings (AudioProviderSettings | VideoProviderSettings): The settings for the provider

        Returns:
             details of rendered avatar instance
        """
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
