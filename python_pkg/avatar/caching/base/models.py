from pydantic import BaseModel, model_validator, ConfigDict
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
from avatar.persona_provider.models import AvatarType, Metadata, Viseme, WordTimestamp

class ContentType(Enum):
    MP4 = 'video/mp4'
    MP3 = 'audio/mpeg'
    WAV = 'audio/wav'
    WEBM = 'video/webm'
    JSON = 'application/json'

EXTENSION_MAPPING = {
    ContentType.MP4: '.mp4',
    ContentType.MP3: '.mp3',
    ContentType.WAV: '.wav',
    ContentType.WEBM: '.webm',
    ContentType.JSON: '.json'
}
class PathType(Enum):
    MEDIA = 'media'
    VISEMES = 'visemes'
    WORD_TIMESTAMPS = 'word_timestamps'
class StoragePaths(BaseModel):
    media_path: str
    viseme_path: Optional[str]
    word_timestamp_path: Optional[str]

    
class DataToStore(BaseModel):
    data_type: AvatarType
    binary_data: bytes
    content_type: ContentType
    visemes:  Optional[List[Viseme]] = None
    word_timestamps: Optional[List[WordTimestamp]] = None
    metadata: Optional[Metadata] = None
    
    """
    validate data type, if it is audio then visemes must also be there
    """
    @model_validator(mode="after")
    def validate_data_type(cls, data):
        if data.data_type == AvatarType.AUDIO and data.visemes is None:
            raise ValueError("Visemes must be present for audio data")
        return data

class Record(BaseModel):
    """
    A single cache record in the database
    """
    model_config = ConfigDict(from_attributes = True)
    
    key: str    # unique key (also filename) for the file stored in storage.
    avatarId: str   # unique key for the avatar, also the folder in storage
    text: str   # text to be converted to audio/video
    storage_paths: StoragePaths
    created: datetime
    updated: Optional[datetime] = None
    isPersonalization: bool = False # whether the text is main message or for personalization
    metadata: Optional[Metadata] = None

    @classmethod
    def from_db(cls, record: Dict) -> "Record":
        return cls(**record)

class UsageLog(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    record_key: str
    timestamp: datetime

    @classmethod
    def from_db(cls, record: Dict) -> "UsageLog":
        return cls(**record)
    

    
