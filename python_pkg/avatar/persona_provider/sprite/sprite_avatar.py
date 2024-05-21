from avatar.persona_provider.base import AvatarType, PersonaBase
from avatar.caching.base.models import ContentType, DataToStore, Metadata
from avatar.persona_provider.models import AudioInstance, AudioProviderSettings
from avatar.tts.base import tts_factory

class SpriteAvatar(PersonaBase):
    """
    Audio avatar class
    """
    async def generate(self, text: str, settings: AudioProviderSettings) -> DataToStore:
        
        audio: AudioInstance = await tts_factory(settings).synthesize_speech(text, settings=settings)
        
        return DataToStore(
            binary_data=audio.content,
            content_type=ContentType.MP3,
            data_type=AvatarType.AUDIO,
            visemes=audio.visemes,
            word_timestamps=audio.word_timestamps,
            metadata = Metadata(
                bit_rate_kbp = settings.bit_rate_kbps,
                sampling_rate_hz = settings.sampling_rate_hz,
                duration_seconds = audio.duration_seconds
            )
        )
        

        