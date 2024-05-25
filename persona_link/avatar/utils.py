from persona_link.avatar.models import Avatar, AvatarInput, WebhookResponseData
from persona_link.cache import Cache
from persona_link.persona_provider import PersonaBase
from persona_link.persona_provider.models import SpeakingAvatarInstance

async def speak(avatar_slug: str, cache: Cache, input: AvatarInput) -> SpeakingAvatarInstance:
    avatar: Avatar = await Avatar.get_or_none(slug=avatar_slug)
    if avatar is None:
        raise ValueError(f"Avatar '{avatar_slug}' not found")
    instance: PersonaBase = avatar.instance()
    settings = instance.validate(avatar.settings)
    if not settings:
        raise ValueError(f"Settings for provider '{avatar.provider}' are invalid")
    
    return await instance.speak(cache, avatar.slug, input.text, settings)

async def call_webhook(avatar_slug: str, data: WebhookResponseData):
    avatar: Avatar = await Avatar.get_or_none(slug=avatar_slug)
    if avatar is None:
        raise ValueError(f"Avatar '{avatar_slug}' not found")
    
    await avatar.fetch_related('webhook')
    if avatar.webhook is None:
        return
    await avatar.webhook.call(data)