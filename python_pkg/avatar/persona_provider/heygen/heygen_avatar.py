from avatar.persona_provider.models import AvatarType, SpeakingAvatarInstance
from avatar.persona_provider.base import PersonaBase
import asyncio
from avatar.api_client import APIClient
from avatar.persona_provider.heygen.models import HeygenAvatarSettings


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
                        raise Exception(f"Video processing failed with error: {result['data']['error']['message']}")
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
                        "avatar_id": settings.heygen_id,
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

    async def generate(self, text: str, settings: HeygenAvatarSettings) -> SpeakingAvatarInstance:
        """
        Speak the given text
        """

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": settings.api_token
        }

        payload = self.formPayload(text, settings)
        result = await APIClient().post_request(self.generate_url, headers, payload)
        
        if "error" in result and result["error"] is not None:
            print(f"Error in response: {result['error']}")
            return None
        video_id = result["data"]["video_id"]

        retrieve_url = f"{self.retrieve_url}?video_id={video_id}"
        video_url = await self.get_video_url(retrieve_url, headers)

        return SpeakingAvatarInstance(
            avatar_type = AvatarType.VIDEO,
            streaming = True,
            content = await APIClient().download(video_url)
        )