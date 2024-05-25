from io import BytesIO

from persona_link.persona_provider.models import (
    AudioInstance,
    Viseme,
    WordTimestamp,
    AudioFormat,
)
from persona_link.tts.base import TTSBase
from persona_link.tts.azure.models import AzureTTSVoiceSettings

from azure.cognitiveservices.speech import (
    SpeechSynthesisOutputFormat,
    SpeechSynthesizer,
    ResultReason,
    SpeechSynthesisBoundaryType,
    SpeechConfig,
    SpeechSynthesisVisemeEventArgs,
    SpeechSynthesisWordBoundaryEventArgs,
    SpeechSynthesisResult,
)


class AzureTTS(TTSBase):
    """
    Azure TTS provider
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AzureTTS, cls).__new__(cls)
        return cls._instance

    def getAudioFormat(
        self, settings: AzureTTSVoiceSettings
    ) -> SpeechSynthesisOutputFormat:
        if settings.format == AudioFormat.MP3:
            if settings.sampling_rate_hz == 16000 and settings.bit_rate_kbps == 32:
                return SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
            elif settings.sampling_rate_hz == 16000 and settings.bit_rate_kbps == 128:
                return SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3
            elif settings.sampling_rate_hz == 16000 and settings.bit_rate_kbps == 64:
                return SpeechSynthesisOutputFormat.Audio16Khz64KBitRateMonoMp3
            elif settings.sampling_rate_hz == 24000 and settings.bit_rate_kbps == 48:
                return SpeechSynthesisOutputFormat.Audio24Khz48KBitRateMonoMp3
            elif settings.sampling_rate_hz == 24000 and settings.bit_rate_kbps == 96:
                return SpeechSynthesisOutputFormat.Audio24Khz96KBitRateMonoMp3
            elif settings.sampling_rate_hz == 24000 and settings.bit_rate_kbps == 160:
                return SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
            elif settings.sampling_rate_hz == 48000 and settings.bit_rate_kbps == 96:
                return SpeechSynthesisOutputFormat.Audio48Khz96KBitRateMonoMp3
            elif settings.sampling_rate_hz == 48000 and settings.bit_rate_kbps == 192:
                return SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
        elif settings.format == AudioFormat.WAV:
            if settings.sampling_rate_hz == 8000:
                return SpeechSynthesisOutputFormat.Riff8Khz16BitMonoPcm
            elif settings.sampling_rate_hz == 16000:
                return SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
            elif settings.sampling_rate_hz == 24000:
                return SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm
            elif settings.sampling_rate_hz == 48000:
                return SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm
            elif settings.sampling_rate_hz == 22050:
                return SpeechSynthesisOutputFormat.Riff22050Hz16BitMonoPcm
            elif settings.sampling_rate_hz == 44100:
                return SpeechSynthesisOutputFormat.Riff44100Hz16BitMonoPcm
        elif settings.format == AudioFormat.OPUS:
            if settings.sampling_rate_hz == 16000:
                return SpeechSynthesisOutputFormat.Ogg16Khz16BitMonoOpus
            elif settings.sampling_rate_hz == 24000:
                return SpeechSynthesisOutputFormat.Ogg24Khz16BitMonoOpus
            elif settings.sampling_rate_hz == 48000:
                return SpeechSynthesisOutputFormat.Ogg48Khz16BitMonoOpus

        raise ValueError("Invalid audio format, sampling rate, or bit rate.")

    async def synthesize_speech(
        self, text: str, settings: AzureTTSVoiceSettings
    ) -> AudioInstance:
        """
        Get the audio bytes for the given text
        """
        try:

            speech_config = SpeechConfig(
                subscription=settings.subscription_key, region=settings.region
            )
            speech_config.set_speech_synthesis_output_format(
                SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
            )
            speech_config.speech_synthesis_voice_name = settings.name
            speech_config.speech_synthesis_language = settings.language
            speech_synthesizer = SpeechSynthesizer(
                speech_config=speech_config, audio_config=None
            )

            visemes = []
            if settings.visemes:

                def viseme_cb(evt: SpeechSynthesisVisemeEventArgs):
                    visemes.append(
                        Viseme(offset=evt.audio_offset / 10000, viseme=evt.viseme_id)
                    )

                speech_synthesizer.viseme_received.connect(viseme_cb)

            word_timestamps = []
            if settings.word_timestamps:

                def word_boundary_cb(evt: SpeechSynthesisWordBoundaryEventArgs):
                    if evt.boundary_type == SpeechSynthesisBoundaryType.Word:
                        word_timestamps.append(
                            WordTimestamp(
                                word=evt.text,
                                offset=evt.audio_offset / 10000,
                                duration=evt.duration.total_seconds() * 1000,
                                text_offset=evt.text_offset,
                                word_length=evt.word_length,
                            )
                        )

                speech_synthesizer.synthesis_word_boundary.connect(word_boundary_cb)

            result: SpeechSynthesisResult = speech_synthesizer.speak_text_async(
                text
            ).get()
            if result.reason != ResultReason.SynthesizingAudioCompleted:
                raise Exception(f"Speech synthesis failed: {result.reason}")

            return AudioInstance(
                streaming=settings.streaming,
                duration_seconds=result.audio_duration.total_seconds(),
                content=(
                    result.audio_data
                    if not settings.streaming
                    else BytesIO(result.audio_data)
                ),
                visemes=visemes if settings.visemes else None,
                word_timestamps=word_timestamps if settings.word_timestamps else None,
            )

        except Exception as e:
            # traceback
            import traceback

            tb = traceback.format_exc()
            raise Exception(f"Error in Azure TTS: {tb}")
