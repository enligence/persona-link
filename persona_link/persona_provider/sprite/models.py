from typing import Optional

from pydantic import BaseModel, ValidationError

from persona_link.persona_provider.models import AudioProviderSettings


class SpriteAvatarSettings(BaseModel):
    """
    Settings for Sprite Avatar Provider. 
    
    Attributes:
        sprite_image_url (str): URL of the sprite image
        eye_blink_url (str): URL of the eye blink image
        image_height (int): Height of the image. Defaults to 256.
        image_width (int): Width of the image. Defaults to 256.
    """
    sprite_image_url: str
    eye_blink_url: str
    image_height: int = 256
    image_width: int = 256
    audio_settings: AudioProviderSettings
    
    @classmethod
    def validate(cls, settings: dict) -> Optional['SpriteAvatarSettings']:
        """
        Validates the settings passed in
        
        Parameters:
            settings (dict): The settings to validate
                
        Returns:
            The settings for the Sprite Avatar Provider if the settings are valid, None otherwise
        """
        try:
            audio_settings = AudioProviderSettings.get_provider(settings["audio_settings"])
            # clone settings and remove audio_settings
            settings = settings.copy()
            settings.pop("audio_settings")
            return cls(**settings, audio_settings=audio_settings)  # Attempts to parse and validate the passed in settings
        except ValidationError:
            return None