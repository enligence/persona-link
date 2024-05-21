from abc import ABC, abstractmethod
from avatar.persona_provider.models import AudioInstance, AudioProviderSettings
from avatar.tts.azure.models import AzureTTSVoiceSettings
    
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
    
def tts_factory(settings: AudioProviderSettings) -> TTSBase:
    """
    Factory method to get the TTS provider
    """
    if isinstance(settings, AzureTTSVoiceSettings):
        from avatar.tts.azure.azure_tts import AzureTTS
        return AzureTTS()
    else:
        raise ValueError("Invalid TTS provider")