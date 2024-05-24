from pydantic import BaseModel, ValidationError
from persona_link.persona_provider.models import VideoFormat, VideoCodecs
from enum import Enum
from typing import Optional
class AzureAvatarStyle(Enum):
    GRACEFUL = "graceful"
    CASUAL = "casual"
    TECHNICAL = "technical"


class AzureAvatarPose(Enum):
    SITTING = "sitting"
    STANDING = "standing"


class AzureAvatarSettings(BaseModel):
    voice: str = "en-IN-NeerjaNeural"
    character: str = "lisa"
    style: AzureAvatarStyle = AzureAvatarStyle.GRACEFUL
    pose: AzureAvatarPose = AzureAvatarPose.SITTING
    video_format: VideoFormat = VideoFormat.WEBM
    background_color: str = "#00000000"
    video_codec:VideoCodecs = VideoCodecs.VP9
    
    @classmethod
    def validate(cls, settings: dict) -> Optional['AzureAvatarSettings']:
        try:
            return cls(**settings)  # Attempts to parse and validate the passed in settings
        except ValidationError as e:
            return None