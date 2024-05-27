from persona_link.tts import AzureTTSVoiceSettings, TTSBase
from persona_link.persona_provider.models import AudioProviderSettings

def tts_factory(settings: AudioProviderSettings) -> TTSBase:
    """
    Factory method to get the TTS provider
    
    Parameters:
        settings (AudioProviderSettings): The settings for the TTS provider
        
    Returns:
        TTSBase: The TTS provider instance
    """
    if isinstance(settings, AzureTTSVoiceSettings):
        from persona_link.tts.azure.azure_tts import AzureTTS
        return AzureTTS()
    else:
        raise ValueError("Invalid TTS provider")
    
def tts_validate(settings: dict) -> AudioProviderSettings:
    """
    Validates the TTS settings
    
    Arguments:
        settings (dict): The settings for the TTS provider
        
    Returns:
        AudioProviderSettings: The validated settings
    """
    return AzureTTSVoiceSettings.validate(settings)