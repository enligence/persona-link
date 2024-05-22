from persona_link.persona_provider.base import AvatarType, PersonaBase
from persona_link.caching.models import ContentType, DataToStore, Metadata
from persona_link.persona_provider.models import AudioInstance, AudioProviderSettings
from persona_link.tts import tts_factory

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
        

        