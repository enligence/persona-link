import asyncio
import os

from persona_link.api_client import APIClient
from persona_link.cache.models import ContentType, DataToStore, Metadata
from persona_link.persona_provider import persona_link_provider
from persona_link.persona_provider.base import PersonaBase
from persona_link.persona_provider.models import (AvatarType,
                                                  SpeakingAvatarInstance)

from .models import HeygenAvatarSettings


@persona_link_provider
class HeygenAvatar(PersonaBase):
    """
    Heygen video avatar provider.
    """

    name = "Heygen"
    description = "Heygen Avatar"

    @classmethod
    def validate(cls, settings: dict) -> HeygenAvatarSettings | None:
        """
        Validate the settings for the provider. This method should return the settings object if the settings are valid

        Parameters:
            settings (dict): The settings for the provider

        Returns:
            Video avatar settings for heygen provider if the settings are valid, None otherwise
        """
        return HeygenAvatarSettings.validate(settings)

    def __init__(self):
        self.generate_url = "https://api.heygen.com/v2/video/generate"
        self.retrieve_url = "https://api.heygen.com/v1/video_status.get"
        self.api_token = os.getenv("HEYGEN_API_TOKEN")

    async def _get_video_url(self, url, headers) -> str:
        try:
            while True:
                result = await APIClient().get_request(url, headers)
                if "code" in result and result["code"] == 100:
                    status = result["data"]["status"]
                    if status == "completed":
                        return result["data"]["video_url"]
                    elif status == "failed":
                        raise Exception(
                            f"Video processing failed with error: {result['data']['error']['message']}"
                        )
                    else:
                        await asyncio.sleep(1)
                else:
                    raise Exception(f"Unexpected response: {result}")
        except Exception as e:
            print(f"Request failed: {str(e)}")
            return None

    def _formPayload(self, text: str, settings: HeygenAvatarSettings) -> dict:
        bg = {"type": settings.background_type}
        if settings.background_type == "color":
            bg["value"] = settings.background_color
        elif settings.background_type == "image":
            bg["image_asset_id"] = settings.background_asset_id
        elif settings.background_type == "video":
            bg["video_asset_id"] = settings.background_asset_id
            bg["play_style"] = "loop"

        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": settings.heygen_id,
                        "avatar_style": settings.avatar_style,
                    },
                    "voice": {
                        "type": "text",
                        "input_text": text,
                        "voice_id": settings.voice_id,
                    },
                    "background": bg,
                }
            ],
            "dimension": {"width": settings.width, "height": settings.height},
            "test": settings.test,
            "caption": False,
        }

        # return as json string
        return payload

    async def generate(
        self, text: str, settings: HeygenAvatarSettings
    ) -> SpeakingAvatarInstance:
        """
        Generate the video for the avatar

        Parameters:
            text (str): The text to be spoken by the avatar
            settings (HeygenAvatarSettings): The settings for the provider

        Returns:
            Rendered video details if successful, None otherwise
        """

        headers = {"Content-Type": "application/json", "X-Api-Key": self.api_token}

        payload = self._formPayload(text, settings)

        result = await APIClient().post_request(self.generate_url, headers, payload)

        if "error" in result and result["error"] is not None:
            print(f"Error in response: {result['error']}")
            return None

        video_id = result["data"]["video_id"]

        retrieve_url = f"{self.retrieve_url}?video_id={video_id}"
        video_url = await self._get_video_url(retrieve_url, headers)


        content = APIClient().download(video_url)

        return DataToStore(
            binary_data=content,
            content_type=ContentType.MP4,
            data_type=AvatarType.VIDEO,
            metadata=Metadata(
                width=settings.width,
                height=settings.height,
            ),
        )
