from pydantic import ValidationError

from persona_link.persona_provider.models import AudioProviderSettings


class AzureTTSVoiceSettings(AudioProviderSettings):
    
    """
    Settings for Azure TTS Voice Provider.
    
    Attributes:
        provider_name (str) : Name of the provider - must be azure
        subscription_key (str) : Subscription key for the Azure service
        region (str) : Region for the Azure service
        name (str) : Name of the voice
        language (str) : Language of the voice
    """
    provider_name: str = "azure"
    name: str
    language: str = "en-US"

    @classmethod
    def validate(cls, settings: dict) -> AudioProviderSettings:
        """
        Validate the settings for the provider. This method should return True if the settings are valid
        
        Parameters:
            settings (dict): The settings for the provider
            
        Returns:
            AudioProviderSettings: The validated settings
        """
        return cls(**settings)  # Attempts to parse and validate the passed in settings