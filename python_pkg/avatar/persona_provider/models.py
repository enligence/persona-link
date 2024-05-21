from enum import Enum
from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Optional
from pydantic import BaseModel, ConfigDict

class AvatarType(Enum):
    AUDIO = 'audio'
    VIDEO = 'video'
     
class Metadata(BaseModel):
    duration_seconds: Optional[float] = None
    sampling_rate_hz: Optional[int] = None
    bit_rate_kbps: Optional[int] = None
    frame_rate: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    
class Urls(BaseModel):
    """
    A class to store the urls for the cached files
    """
    media_url: str
    viseme_url: Optional[str] = None
    word_timestamp_url: Optional[str] = None
class SpeakingAvatarInstance(BaseModel):
    avatar_type: AvatarType = AvatarType.AUDIO
    urls: Urls
    metadata: Optional[Metadata] = None

class VideoFormat(str, Enum):
    MP4 = "mp4"
    WEBM = "webm"
    OGG = "ogg"

class CommonVideoSettings(BaseModel):
    word_timestamps: bool = False
    streaming: bool = False
    frame_rate: int = 30
    width: int = 640
    height: int = 480
    video_format: VideoFormat = VideoFormat.MP4

class VideoProviderSettings(CommonVideoSettings, ABC):
    @abstractmethod
    def validate(self) -> bool:
        pass

class Viseme(BaseModel):
    offset: int # in milliseconds
    viseme: int # viseme id as in https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-speech-synthesis-viseme?tabs=visemeid&pivots=programming-language-python#map-phonemes-to-visemes

class WordTimestamp(BaseModel):
    word: str # word spoken
    offset: int # in milliseconds
    duration: int # in milliseconds
    text_offset: int # offset in text
    word_length: int # length of the word spoken
class AudioInstance(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed = True)  #skip the validation for any custom/unrecognized types. like AsyncGenerator
    duration_seconds: Optional[float] = None
    streaming: bool = False
    content: bytes | AsyncGenerator[bytes, None]
    visemes: Optional[List[Viseme]]
    word_timestamps: Optional[List[WordTimestamp]]
    
class AudioFormat(str, Enum):
    MP3 = "mp3"
    WAV = "wav"
    OPUS = "opus"

class CommonAudioSettings(BaseModel):
    visemes: bool = False
    word_timestamps: bool = False
    streaming: bool = False
    sampling_rate_hz: int = 16000
    bit_rate_kbps: int = 32
    audio_format: AudioFormat = AudioFormat.MP3

class AudioProviderSettings(CommonAudioSettings, ABC):
    @abstractmethod
    def validate(self) -> bool:
        pass 