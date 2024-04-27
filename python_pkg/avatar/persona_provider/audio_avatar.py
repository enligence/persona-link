from python_pkg.avatar.persona_provider.base import AvatarType, PersonaBase, SpokenAvatarInstance, TTSBase


class AudioAvatar(PersonaBase):
    """
    Audio avatar class
    """
    def __init__(self, tts_provider: TTSBase):
        self.tts = tts_provider

    async def speak(self, text: str, settings: dict = {}) -> SpokenAvatarInstance:
        """
        Speak the given text
        """
        result = self.tts.synthesize_speech(text, settings)
        return SpokenAvatarInstance(
            avatar_type = AvatarType.AUDIO,
            streaming = result.streaming,
            content = result.content,
            visemes = result.visemes
        )