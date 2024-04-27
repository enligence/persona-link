from io import BytesIO
from python_pkg.avatar.persona_provider.base import AudioInstance, TTSBase
import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesisVisemeEventArgs
import azure.cognitiveservices.speech as speechsdk
from pydantic import BaseModel

class AzureTTSVoiceSettings(BaseModel):
    subscription_key: str
    region: str
    name: str
    language: str = "en-US"

class AzureTTS(TTSBase):
    """
    Azure TTS provider
    """
    def __init__(self):
        pass
        

    async def synthesize_speech(self, text: str, settings: dict = {}) -> AudioInstance:
        """
        Get the audio bytes for the given text
        """
        try:
            voice_settings = AzureTTSVoiceSettings(**settings)

            speech_config = SpeechConfig(subscription=voice_settings.subscription_key, region=voice_settings.region)
            speech_config.speech_synthesis_voice_name = voice_settings.name
            speech_config.speech_synthesis_language = voice_settings.language
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

            if settings.get("visemes", False):
                visemes = []
                def viseme_cb(evt: SpeechSynthesisVisemeEventArgs):
                    viseme_info = {
                        "offset": evt.audio_offset/10000,
                        "viseme": evt.viseme_id
                    }
                    visemes.append(viseme_info)

                speech_synthesizer.viseme_received.connect(viseme_cb)


            result = speech_synthesizer.speak_text_async(text).get()
            if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
                raise Exception(f"Speech synthesis failed: {result.reason}")
            
            stream = settings.get("streaming", False)
            return AudioInstance(
                streaming = stream,
                content = result.audio_data if stream else BytesIO(result.audio_data),
                visemes = visemes if settings.get("visemes", False) else None
            )
        except Exception as e:
            raise Exception(f"Error in Azure TTS: {str(e)}")