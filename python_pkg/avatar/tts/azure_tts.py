from io import BytesIO
from avatar.tts.base import TTSBase
from avatar.tts.models import AudioInstance, Viseme, WordTimestamp
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesisVisemeEventArgs, SpeechSynthesisWordBoundaryEventArgs
import azure.cognitiveservices.speech as speechsdk
from pydantic import BaseModel

class AzureTTSVoiceSettings(BaseModel):
    subscription_key: str
    region: str
    name: str
    language: str = "en-US"
    visemes: bool = False
    word_timestamps: bool = False
    streaming: bool = False

class AzureTTS(TTSBase):
    """
    Azure TTS provider
    """
    def __init__(self):
        pass
        

    async def synthesize_speech(self, text: str, settings: AzureTTSVoiceSettings) -> AudioInstance:
        """
        Get the audio bytes for the given text
        """
        try:

            speech_config = SpeechConfig(subscription=settings.subscription_key, region=settings.region)
            speech_config.speech_synthesis_voice_name = settings.name
            speech_config.speech_synthesis_language = settings.language
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
            
            visemes = []
            if settings.visemes:
                def viseme_cb(evt: SpeechSynthesisVisemeEventArgs):
                    visemes.append(Viseme(offset = evt.audio_offset/10000, viseme = evt.viseme_id))

                speech_synthesizer.viseme_received.connect(viseme_cb)
                
            word_timestamps = []
            if settings.word_timestamps:
                def word_boundary_cb(evt: SpeechSynthesisWordBoundaryEventArgs):
                    if evt.boundary_type == speechsdk.SpeechSynthesisBoundaryType.Word:
                        word_timestamps.append(WordTimestamp(
                            word = evt.text,
                            offset = evt.audio_offset / 10000,
                            duration = evt.duration.total_seconds()*1000,
                            text_offset = evt.text_offset,
                            word_length = evt.word_length
                        ))

                speech_synthesizer.synthesis_word_boundary.connect(word_boundary_cb)


            result = speech_synthesizer.speak_text_async(text).get()
            if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
                raise Exception(f"Speech synthesis failed: {result.reason}")
            
            return AudioInstance(
                streaming = settings.streaming,
                content = result.audio_data if not settings.streaming else BytesIO(result.audio_data),
                visemes = visemes if settings.visemes else None,
                word_timestamps = word_timestamps if settings.word_timestamps else None
            )
            
        except Exception as e:
            # traceback
            import traceback
            tb = traceback.format_exc()
            raise Exception(f"Error in Azure TTS: {tb}")