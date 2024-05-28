from .models import Avatar, AvatarInput, WebhookResponseData
from persona_link.cache import Cache
from persona_link.persona_provider import PersonaBase
from persona_link.persona_provider.models import AudioProviderSettings, AvatarType, SpeakingAvatarInstance

async def get_avatar_info(avatar_slug: str) -> Avatar:
    """
    Get the avatar with the given slug
    
    Parameters:
        avatar_slug (str): The slug of the avatar to get
        
    Returns:
        A tuple with the following values:
            Avatar: The avatar with the given slug
            AvatarType: The type of the avatar
    """
    avatar: Avatar = await Avatar.get_or_none(slug=avatar_slug)
    if avatar is None:
        raise ValueError(f"Avatar '{avatar_slug}' not found")
    instance: PersonaBase = avatar.instance()
    settings = instance.validate(avatar.settings)
    if not settings:
        raise ValueError(f"Settings for provider '{avatar.provider}' are invalid")
    
    if isinstance(settings, AudioProviderSettings):
        return avatar, AvatarType.AUDIO.value
    else:
        return avatar, AvatarType.VIDEO.value
    

async def speak(avatar_slug: str, cache: Cache, input: AvatarInput) -> SpeakingAvatarInstance:
    """
    Speak the input text using the avatar with the given slug
    
    Parameters:
        avatar_slug (str): The slug of the avatar to use
        cache (Cache): The cache object to use
        input (AvatarInput): The input text to speak
        
    Returns:
        SpeakingAvatarInstance: The instance of the speaking avatar
    """
    avatar: Avatar = await Avatar.get_or_none(slug=avatar_slug)
    if avatar is None:
        raise ValueError(f"Avatar '{avatar_slug}' not found")
    instance: PersonaBase = avatar.instance()
    settings = instance.validate(avatar.settings)
    if not settings:
        raise ValueError(f"Settings for provider '{avatar.provider}' are invalid")
    
    return await instance.speak(cache, avatar.slug, input.text, settings)

async def call_webhook(avatar_slug: str, data: WebhookResponseData):
    """
    Call the webhook of the avatar with the given slug. 
    The calling app must handle the request and take appropriate action
    
    Parameters:
        avatar_slug (str): The slug of the avatar to use
        data (WebhookResponseData): The data to send to the webhook
    """
    avatar: Avatar = await Avatar.get_or_none(slug=avatar_slug)
    if avatar is None:
        raise ValueError(f"Avatar '{avatar_slug}' not found")
    
    await avatar.fetch_related('webhook')
    if avatar.webhook is None:
        return
    await avatar.webhook.call(data)