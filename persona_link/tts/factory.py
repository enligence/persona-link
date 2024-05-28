from persona_link.persona_provider.models import AudioProviderSettings

from .base import TTSBase


def tts_factory(settings: AudioProviderSettings) -> TTSBase:
    """
    Factory method to get the TTS provider
    
    Parameters:
        settings (AudioProviderSettings): The settings for the TTS provider
        
    Returns:
        TTSBase: The TTS provider instance
    """
    if settings.provider_name == "azure":
        from persona_link.tts.azure.azure_tts import AzureTTS
        return AzureTTS()
    else:
        raise ValueError("Invalid TTS provider")