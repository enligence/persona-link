from datetime import datetime
from enum import Enum
from typing import AsyncGenerator, Dict, List, Optional

from pydantic import BaseModel, ConfigDict

from persona_link.persona_provider.models import (AvatarType, Metadata, Viseme,
                                                  WordTimestamp)


class ContentType(Enum):
    """
    Enum for the content type of the data to be stored
    
    Values:
    ```
        MP4  : MP4 video content type
        MP3  : MP3 audio content type
        WAV  : WAV audio content type
        WEBM : WEBM video content type
        JSON : JSON metadata content type
    ```
    """
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
    """
    Enum for the type of path
    
    Values:
    ```
        MEDIA           : Media path
        VISEMES         : Visemes path
        WORD_TIMESTAMPS : Word timestamps path
    ```
    """
    MEDIA = 'media'
    VISEMES = 'visemes'
    WORD_TIMESTAMPS = 'word_timestamps'
class StoragePaths(BaseModel):
    """
    Model for the storage paths of the data
    
    Attributes:
        media_path (str): Media path
        viseme_path (Optional[str]): Visemes path
        word_timestamp_path (Optional[str]): Word timestamps path
    """
    media_path: str
    visemes_path: Optional[str]
    word_timestamps_path: Optional[str]

    
class DataToStore(BaseModel):
    """
    Model for the data to be stored in the cache
    
    Attributes:
        data_type (AvatarType): Type of the data
        binary_data (bytes | AsyncGenerator[bytes, None]): Binary data to be stored
        content_type (ContentType): Content type of the data
        visemes (Optional[List[Viseme]]): Visemes for the data
        word_timestamps (Optional[List[WordTimestamp]]): Word timestamps for the data
        metadata (Optional[Metadata]): Metadata for the data
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    data_type: AvatarType
    binary_data: bytes | AsyncGenerator[bytes, None]    # binary data to be stored
    content_type: ContentType
    visemes:  Optional[List[Viseme]] = None
    word_timestamps: Optional[List[WordTimestamp]] = None
    metadata: Optional[Metadata] = None

class Record(BaseModel):
    """
    A single cache record in the database
    
    Attributes:
        key (str): unique key (also filename) for the file stored in storage.
        avatarId (str): unique key for the avatar, also the folder in storage
        text (str): text to be converted to audio/video
        storage_paths (StoragePaths): paths where the media and related files are stored
        created (datetime): timestamp when the record was created
        updated (Optional[datetime]): timestamp of the last update of the record
        metadata (Optional[Metadata]): metadata about the record
    """
    model_config = ConfigDict(from_attributes = True)
    
    key: str    # unique key (also filename) for the file stored in storage.
    avatarId: str   # unique key for the avatar, also the folder in storage
    text: str   # text to be converted to audio/video
    storage_paths: StoragePaths
    created: datetime
    updated: Optional[datetime] = None
    metadata: Optional[Metadata] = None

    @classmethod
    def from_db(cls, record: Dict) -> "Record":
        return cls(**record)

class UsageLog(BaseModel):
    """
    A log of usage of a cache record
    
    Attributes:
        record_key (str): the key of the record for which the usage is logged
        timestamp (datetime): timestamp of the usage
    """
    model_config = ConfigDict(from_attributes = True)
    
    record_key: str
    timestamp: datetime

    @classmethod
    def from_db(cls, record: Dict) -> "UsageLog":
        return cls(**record)
    

    
