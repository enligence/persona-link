from pydantic import BaseModel
from persona_link.persona_provider.models import VideoFormat, VideoCodecs
from enum import Enum

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