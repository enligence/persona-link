from abc import ABC, abstractmethod
from python_pkg.avatar.tts.models import AudioInstance

    
class TTSBase(ABC):
    @abstractmethod
    async def synthesize_speech(self, text: str, settings: dict = {}) -> AudioInstance:
        """
        Get the audio bytes for the given text with max 300 words
        if settings have visemes set, then return visemes array too.
        """
        pass