from typing import Optional

from pydantic import ValidationError

from persona_link.persona_provider.models import VideoProviderSettings


class HeygenAvatarSettings(VideoProviderSettings):
    """
    Settings for Heygen Avatar Provider. Refer to [heygen](https://docs.heygen.com/docs/create-video) for more information.
    
    Attributes:
        heygen_id (str): Heygen ID of the Avatar.
        avatar_style (str): Style of the Avatar.
        voice_id (str): ID of the voice.
        background_color (str): Color of the background.
        background_type (str): Type of the background.
        background_asset_id (str): ID of the background asset.
        test (bool): Whether to test the Avatar.
        api_token (str): API token of the Avatar.
    """
    heygen_id: str
    avatar_style: str
    voice_id: str
    background_color: Optional[str] = None
    background_type: str = "color"
    background_asset_id: Optional[str] = None
    test: bool = True
    api_token: str
    
    @classmethod
    def validate(cls, settings: dict) -> Optional['HeygenAvatarSettings']:
        """
        Validates the settings passed in
        
        Parameters:
            settings (dict): The settings to validate
                
        Returns:
            The settings for the Heygen Avatar Provider if the settings are valid, None otherwise
        """
        try:
            return cls(**settings)  # Attempts to parse and validate the passed in settings
        except ValidationError:
            return None
        
    
    

    # @model_validator(mode="after")
    # def validate_background_settings(cls, values):
    #     background_color, background_type, background_asset_id = values.get('background_color'), values.get('background_type'), values.get('background_asset_id')
    #     if background_type == "color" and not background_color:
    #         raise ValueError('background_color must be provided for color background type')
    #     if (background_type == "image" or background_type == "video") and not background_asset_id:
    #         raise ValueError('background_asset_id must be provided for asset background type')
    #     if background_type not in ["color", "image", "video"]:
    #         raise ValueError('background_type must be one of color, image or video')
        
    #     avatar_style = values.get('avatar_style')
    #     if avatar_style not in ["normal", "circle", "closeUp"]:
    #         raise ValueError('avatar_style must be one of normal, circle or closeUp')
    #     return values
