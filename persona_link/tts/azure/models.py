from persona_link.persona_provider.models import AudioProviderSettings
from pydantic import ValidationError
class AzureTTSVoiceSettings(AudioProviderSettings):
    provider_name: str = "azure"
    subscription_key: str
    region: str
    name: str
    language: str = "en-US"

    @classmethod
    def validate(cls, settings: dict) -> bool:
        try:
            _ = cls(**settings)  # Attempts to parse and validate the passed in settings
            return True
        except ValidationError as e:
            return False
    