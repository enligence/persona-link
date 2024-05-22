from abc import ABC, abstractmethod
from persona_link.persona_provider.models import AudioInstance, AudioProviderSettings
    
class TTSBase(ABC):
    @abstractmethod
    async def synthesize_speech(self, text: str, settings: AudioProviderSettings) -> AudioInstance:
        """
        Get the audio bytes for the given text with max 300 words
        if settings have visemes set, then return visemes array too.
        
        TODO: Alternatively, we can also include a text transformer that may generate SSML 
        for text to make it more accurately being spoken.
        Most cloud models are trained well to handle many scenarios but certain scientific 
        and challenging terminologies may still be incorrectly spoken.
        """
        pass