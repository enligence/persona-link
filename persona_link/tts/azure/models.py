from persona_link.persona_provider.models import AudioProviderSettings

class AzureTTSVoiceSettings(AudioProviderSettings):
    subscription_key: str
    region: str
    name: str
    language: str = "en-US"

    def validate(self) -> bool:
        # Perform validation 
        return True
    