from abc import ABC, abstractmethod
from python_pkg.avatar.persona_provider.models import SpokenAvatarInstance


"""
Base class for persona provider
"""
class PersonaBase(ABC):
    @abstractmethod
    async def speak(self, text: str, settings: dict = {}) -> SpokenAvatarInstance:
        """
        Based upon the settings provided, 
        the persona will speak the text.
        For video avatar it should return video bytes or stream
        for audio avatar it should return audio bytes / stream and visemes
        """
        pass
