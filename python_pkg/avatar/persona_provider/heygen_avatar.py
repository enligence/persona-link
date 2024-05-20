from avatar.persona_provider.models import AvatarType, PersonaBase, SpokenAvatarInstance
from pydantic import BaseModel, model_validator
import asyncio
from typing import Optional
from api_client import APIClient

class HeygenAvatarSettings(BaseModel):
    avatar_id: str
    avatar_style: str
    voice_id: str
    background_color: Optional[str] = None
    background_type: str = "color"
    background_asset_id: Optional[str] = None
    width: int = 640
    height: int = 480
    test: bool = True
    api_token: str

    @model_validator(mode="after")
    def validate_background_settings(cls, values):
        background_color, background_type, background_asset_id = values.get('background_color'), values.get('background_type'), values.get('background_asset_id')
        if background_type == "color" and not background_color:
            raise ValueError('background_color must be provided for color background type')
        if (background_type == "image" or background_type == "video") and not background_asset_id:
            raise ValueError('background_asset_id must be provided for asset background type')
        if background_type not in ["color", "image", "video"]:
            raise ValueError('background_type must be one of color, image or video')
        
        avatar_style = values.get('avatar_style')
        if avatar_style not in ["normal", "circle", "closeUp"]:
            raise ValueError('avatar_style must be one of normal, circle or closeUp')
        return values

class HeygenAvatar(PersonaBase):
    """
    Audio avatar class
    """
    def __init__(self):
        self.generate_url = "https://api.heygen.com/v2/video/generate"
        self.retrieve_url = "https://api.heygen.com/v1/video_status.get"

    async def get_video_url(url, headers) -> str:
        try:
            while True:
                result = await APIClient().get_request(url, headers)
                if "code" in result and result["code"] == 100:
                    status = result["data"]["status"]
                    if status == "completed":
                        return result["data"]["video_url"]
                    elif status == "failed":
                        raise Exception(f"Video processing failed with error: {result['data']['error']["message"]}")
                    else:
                        await asyncio.sleep(1)
                else:
                    raise Exception(f"Unexpected response: {result}")
        except Exception as e:
            print(f"Request failed: {str(e)}")
            return None

    def formPayload(self, text: str, settings: HeygenAvatarSettings) -> dict:
        bg = {
            "type": settings.background_type
        }
        if settings.background_type == "color":
            bg["value"] = settings.background_color
        elif settings.background_type == "image":
            bg["image_asset_id"] = settings.background_asset_id
        elif settings.background_type == "video":
            bg["video_asset_id"] = settings.background_asset_id
            bg["play_style"] = "loop"

        return {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": settings.avatar_id,
                        "avatar_style": settings.avatar_style
                    },
                    "voice": {
                        "type": "text",
                        "input_text": text,
                        "voice_id": settings.voice_id
                    },
                    "background": bg
                }
            ],
            "dimension": {
                "width": settings.width,
                "height": settings.height
            },
            "test": settings.test
        }

    async def speak(self, text: str, settings: dict = {}) -> SpokenAvatarInstance:
        """
        Speak the given text
        """

        heygen_settings = HeygenAvatarSettings(**settings)

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": heygen_settings.api_token
        }

        payload = self.formPayload(text, heygen_settings)
        result = await APIClient().post_request(self.generate_url, headers, payload)
        
        if "error" in result and result["error"] is not None:
            print(f"Error in response: {result['error']}")
            return None
        video_id = result["data"]["video_id"]

        retrieve_url = f"{self.retrieve_url}?video_id={video_id}"
        video_url = await self.get_video_url(retrieve_url, headers)

        return SpokenAvatarInstance(
            avatar_type = AvatarType.VIDEO,
            streaming = True,
            content = await APIClient().download(video_url)
        )