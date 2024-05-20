# Enumeration for the type of avatar
from enum import Enum
from pydantic import BaseModel, model_validator, ConfigDict
from io import BytesIO
from typing import AsyncGenerator, List, Optional

from avatar.tts.models import Viseme

class AvatarType(str, Enum):
    """
    Enumeration for the type of avatar
    """
    VIDEO = 'video'
    AUDIO = 'audio'


class SpokenAvatarInstance(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed = True)  #skip the validation for any custom/unrecognized types. like AsyncGenerator
    avatar_type: AvatarType = AvatarType.AUDIO
    streaming: bool = False
    content: bytes | AsyncGenerator[bytes, None]
    visemes: Optional[List[Viseme]]

    @model_validator(mode="after")
    def check_content_and_visemes(cls, values):
        avatar_type, visemes, streaming, content = values.get('avatar_type'), values.get('visemes'), values.get('streaming'), values.get('content')
        if avatar_type == AvatarType.AUDIO and not visemes:
            raise ValueError('visemes must be provided for audio type avatar')
        if streaming and not isinstance(content, AsyncGenerator[bytes, None]):
            raise ValueError('If streaming is True, content must be of BytesIO type')
        return values