from abc import ABC, abstractmethod
from enum import Enum
from typing import AsyncGenerator, List, Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class AvatarType(Enum):
    """
    Enum for the type of avatar

    Values:
    ```
        AUDIO : Audio avatar
        VIDEO : Video avatar
    ```
    """

    AUDIO = "audio"
    VIDEO = "video"


class Metadata(BaseModel):
    """
    A class to store the metadata of the cached files

    Attributes:
        duration_seconds (Optional[float]): Duration of the media in seconds
        sampling_rate_hz (Optional[int]): Sampling rate of the media in Hz
        bit_rate_kbps (Optional[int]): Bit rate of the media in kbps
        frame_rate (Optional[int]): Frame rate of the video
        width (Optional[int]): Width of the video
        height (Optional[int]): Height of the video
    """

    duration_seconds: Optional[float] = None
    sampling_rate_hz: Optional[int] = None
    bit_rate_kbps: Optional[int] = None
    frame_rate: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


class Urls(BaseModel):
    """
    A class to store the urls for the cached files

    Attributes:
        media_url (str): URL of the media
        visemes_url (Optional[str]): URL of the visemes
        word_timestamps_url (Optional[str]): URL of the word timestamps
    """

    media_url: str
    visemes_url: Optional[str] = None
    word_timestamps_url: Optional[str] = None


class SpeakingAvatarInstance(BaseModel):
    """
    A class to store the instance of the speaking avatar

    Attributes:
        avatar_type (AvatarType): Type of the avatar
        urls (Urls): URLs of the cached files
        metadata (Optional[Metadata]): Metadata of the cached files
    """

    avatar_type: AvatarType = AvatarType.AUDIO
    urls: Urls
    metadata: Optional[Metadata] = None


class VideoFormat(str, Enum):
    """
    Enum for the video format

    Values:
    ```
        MP4  : MP4 format
        WEBM : WEBM format
        OGG  : OGG format
    ```
    """

    MP4 = "mp4"
    WEBM = "webm"
    OGG = "ogg"


class VideoCodecs(Enum):
    """
    Enum for the video codecs

    Values:
    ```
        VP9  : VP9 codec
        H264 : H264 codec
        HEVC : HEVC codec
    ```
    """

    VP9 = "vp9"
    H264 = "h264"
    HEVC = "hevc"


class CommonVideoSettings(BaseModel):
    """
    A class to store the common settings for the video

    Attributes:
        word_timestamps (bool): Whether to include word timestamps, default is False
        streaming (bool): Whether to stream the video, default is False
        frame_rate (int): Frame rate of the video, default is 30
        width (int): Width of the video, default is 640
        height (int): Height of the video, default is 480
        video_format (VideoFormat): Format of the video, default is MP4
        video_codec (VideoCodecs): Codec of the video, default is HEVC
    """

    word_timestamps: bool = False
    streaming: bool = False
    frame_rate: int = 30
    width: int = 640
    height: int = 480
    video_format: VideoFormat = VideoFormat.MP4
    video_codec: VideoCodecs = VideoCodecs.HEVC


class VideoProviderSettings(CommonVideoSettings, ABC):
    """
    A class to represent the video provider settings

    Attributes:
        provider_name (str): Name of the provider
    """

    @classmethod
    @abstractmethod
    def validate(cls, settings: dict) -> Optional["VideoProviderSettings"]:
        """
        Validate the settings for the provider. This method should return the settings object if the settings are valid

        Parameters:
            settings (dict): The settings for the provider

        Returns:
            Video provider settings object for the provider
        """
        pass


class Viseme(BaseModel):
    """
    A class to store the viseme

    Attributes:
        offset (int): Offset in milliseconds
        viseme (int): Viseme id as in https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-speech-synthesis-viseme?tabs=visemeid&pivots=programming-language-python#map-phonemes-to-visemes
    """

    offset: int  # in milliseconds
    viseme: int  # viseme id as in https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-speech-synthesis-viseme?tabs=visemeid&pivots=programming-language-python#map-phonemes-to-visemes


class WordTimestamp(BaseModel):
    """
    A class to store the word timestamp

    Attributes:
        word (str): Word spoken
        offset (int): Offset in milliseconds
        duration (int): Duration in milliseconds
        text_offset (int): Offset in text
        word_length (int): Length of the word spoken
    """

    word: str  # word spoken
    offset: int  # in milliseconds
    duration: int  # in milliseconds
    text_offset: int  # offset in text
    word_length: int  # length of the word spoken


class AudioInstance(BaseModel):
    """
    A class to store the audio instance

    Attributes:
        duration_seconds (Optional[float]): Duration of the audio in seconds
        streaming (bool): Whether to stream the audio
        content (bytes | AsyncGenerator[bytes, None]): Content of the audio
        visemes (Optional[List[Viseme]]): List of visemes
        word_timestamps (Optional[List[WordTimestamp]]): List of word timestamps
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )  # skip the validation for any custom/unrecognized types. like AsyncGenerator
    duration_seconds: Optional[float] = None
    streaming: bool = False
    content: bytes | AsyncGenerator[bytes, None]
    visemes: Optional[List[Viseme]]
    word_timestamps: Optional[List[WordTimestamp]]


class AudioFormat(str, Enum):
    """
    Enum for the audio format

    Values:
    ```
        MP3  : MP3 format
        WAV  : WAV format
        OPUS : OPUS format
    ```
    """

    MP3 = "mp3"
    WAV = "wav"
    OPUS = "opus"


class CommonAudioSettings(BaseModel):
    """
    A class to store the common settings for the audio

    Attributes:
        visemes (bool): Whether to include visemes, default is False
        word_timestamps (bool): Whether to include word timestamps, default is False
        streaming (bool): Whether to stream the audio, default is False
        sampling_rate_hz (int): Sampling rate of the audio in Hz, default is 16000
        bit_rate_kbps (int): Bit rate of the audio in kbps, default is 32
        audio_format (AudioFormat): Format of the audio, default is MP3
    """

    visemes: bool = False
    word_timestamps: bool = False
    streaming: bool = False
    sampling_rate_hz: int = 16000
    bit_rate_kbps: int = 32
    audio_format: AudioFormat = AudioFormat.MP3


registered_audio_provider_settings = {}


class AudioProviderSettings(CommonAudioSettings, ABC):
    """
    A class to represent the audio provider settings

    Attributes:
        provider_name (str): Name of the provider
    """

    provider_name: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not cls.provider_name:
            raise ValueError("Provider name is required")

        registered_audio_provider_settings[cls.provider_name] = cls

    @classmethod
    def get_provider(cls, settings: dict) -> Optional["AudioProviderSettings"]:
        """
        Get the provider for the settings

        Parameters:
            settings (dict): The settings for the provider

        Returns:
            Audio provider settings object for the provider
        """
        try:
            Provider = registered_audio_provider_settings.get(settings.get("provider_name"))
            return Provider.validate(settings)
        except (ValidationError, AttributeError) as e:
            raise ValueError("Provider not found or bad configuration", str(e))

    @classmethod
    @abstractmethod
    def validate(cls, settings: dict) -> Optional["AudioProviderSettings"]:
        """
        Validate the settings for the provider. This method should return the settings object if the settings are valid

        Parameters:
            settings (dict): The settings for the provider

        Returns:
            Audio provider settings object for the provider
        """
        pass
