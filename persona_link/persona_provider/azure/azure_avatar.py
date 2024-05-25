from persona_link.persona_provider import persona_link_provider
from persona_link.persona_provider.models import (
    AvatarType,
    SpeakingAvatarInstance
)
from persona_link.persona_provider.base import PersonaBase
import asyncio
from persona_link.api_client import APIClient
import os
from persona_link.cache.models import ContentType, DataToStore, Metadata
from uuid import uuid4
from persona_link.persona_provider.azure.models import AzureAvatarSettings
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech-avatar/what-is-text-to-speech-avatar
@persona_link_provider
class AzureAvatar(PersonaBase):
    """
    Audio avatar class
    """
    name = "Azure"
    description = "Azure Avatar"
    
    @classmethod
    def validate(cls, settings: dict) -> AzureAvatarSettings | None:
        return AzureAvatarSettings.validate(settings)
    
    def __init__(self):
        self.speech_endpoint = os.getenv("AZURE_AVATAR_ENDPOINT")
        self.api_version = os.getenv("AZURE_AVATAR_API_VERSION")
        self.subscription_key = os.getenv("AZURE_AVATAR_SUBSCRIPTION_KEY")

        self.headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.subscription_key,
        }

    def generate_url(self, job_id: str) -> str:
        return f"{self.speech_endpoint}/avatar/batchsyntheses/{job_id}?api-version={self.api_version}"

    async def get_video_url(self, url: str) -> str:
        try:
            while True:
                result = await APIClient().get_request(url, self.headers)
                #print(result)
                if "status" in result and result["status"] == "Succeeded":
                    return result["outputs"]["result"]
                else:
                    await asyncio.sleep(1)
        except Exception as e:
            print(f"Request failed: {str(e)}")
            return None

    def formPayload(self, text: str, settings: AzureAvatarSettings) -> dict:

        payload = {
            "synthesisConfig": {"voice": settings.voice},
            "inputKind": "plainText",
            "inputs": [
                {"content": text},  # in future we can optimize by doing actual batches
            ],
            "avatarConfig": {
              "customized": False, # set to True if you want to use customized avatar
              "talkingAvatarCharacter": f"{settings.character}",  # talking avatar character
              "talkingAvatarStyle": f"{settings.style.value}-{settings.pose.value}",  # talking avatar style
              "videoFormat": settings.video_format.value,  # mp4 or webm, webm is required for transparent background
              "videoCodec": settings.video_codec.value,  # hevc, h264 or vp9, vp9 is required for transparent background; default is hevc
              "subtitleType": "soft_embedded",
              "backgroundColor": settings.background_color,
            }
        }
        # return as json string
        return payload

    async def generate(
        self, text: str, settings: AzureAvatarSettings
    ) -> SpeakingAvatarInstance:
        """
        Speak the given text
        """

        payload = self.formPayload(text, settings)
        job_id = uuid4().hex
        url = self.generate_url(job_id)
        result = await APIClient().put_request(url, self.headers, payload)
        if not "id" in result:
            print(f"Error in response: {result}")
            return None
        bitrate_kbps = result["avatarConfig"]["bitrateKbps"]
        video_url = await self.get_video_url(url)

        content = APIClient().download(video_url)

        return DataToStore(
            binary_data=content,
            content_type=ContentType.MP4,
            data_type=AvatarType.VIDEO,
            metadata=Metadata(
                width=1920,
                height=1080,
                bit_rate_kbps=bitrate_kbps,
                frame_rate=25
            ),
        )
