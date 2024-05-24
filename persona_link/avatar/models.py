from tortoise.models import Model
from tortoise import fields
from persona_link.persona_provider import persona_link_providers
from persona_link.persona_provider.models import AvatarType
from persona_link.api_client import APIClient
from enum import Enum
from pydantic import BaseModel
from typing import Optional

ProviderEnum = Enum('ProviderEnum', {k:k for k in persona_link_providers.keys()})

class WebhookResponseData(BaseModel):
    text: Optional[str] = None
    media_url: Optional[str] = None
    media_type: Optional[AvatarType] = None
    conversation_id: str # id that the source will use to determining conversation details
    
class AvatarInput(BaseModel):
    text: str # text to speak
    personalize: bool = False # whether to personalize the avatar

class WebhookPydantic(BaseModel):
    url: str
    headers: Optional[dict] = None
    method: Optional[str] = "POST"
    get_text: bool = True
    get_audio: bool = False
    get_video: bool = False
    video_width: Optional[int] = 320
    video_height:  Optional[int] = 240
    video_frame_rate:  Optional[int] = 25
    audio_bit_rate:  Optional[int] = 32
    audio_sampling_rate:  Optional[int] = 22050

class Webhook(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(255)
    headers = fields.JSONField(null=True)
    method = fields.CharField(10, default="POST")
    get_text = fields.BooleanField(default=True)
    get_audio = fields.BooleanField(default=False)
    get_video = fields.BooleanField(default=False)
    video_width = fields.IntField(default = 320)
    video_height = fields.IntField(default = 240)
    video_frame_rate = fields.IntField(default = 25)
    audio_bit_rate = fields.IntField(default = 32)
    audio_sampling_rate = fields.IntField(default = 22050)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    async def call(self, data: WebhookResponseData):
        # make a request to the webhook url
        await APIClient().post_request(self.url, self.headers, data.model_dump())
    
    class Meta:
        table = "webhooks"
        app = "persona_link"
        
class AvatarPydantic(BaseModel):
    name: str
    provider: str
    settings: dict
    
class Avatar(Model):
    id = fields.IntField(pk=True, description="Primary Key")
    name = fields.CharField(255, description="Name for the avatar")
    slug = fields.CharField(255, unique=True, description="Auto-generated unique identifier")
    provider = fields.CharEnumField(ProviderEnum, description="Provider for the avatar") # for factory method
    settings = fields.JSONField(description="Settings for the avatar") # these settings will be validated by the provider
    webhook = fields.ForeignKeyField('persona_link.Webhook', related_name='avatars', description="Webhook to send the avatar to", null=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="Creation timestamp")
    updated_at = fields.DatetimeField(auto_now=True, description="Last update timestamp")
    
    def instance(self):
        return persona_link_providers[self.provider]()
    
    @classmethod
    async def create_avatar(cls, data: AvatarPydantic, webhook: WebhookPydantic | None = None):
        if data.provider not in persona_link_providers:
            raise ValueError(f"Provider '{data.provider}' not found")
        
        provider = persona_link_providers[data.provider]
        if not provider.validate(data.settings):
            raise ValueError(f"Settings for provider '{data.provider}' are invalid")
        
        w = None
        if webhook is not None:
            w = await Webhook.create(**webhook.model_dump())
        
        base_slug = slug = data.name.lower().replace(' ', '-')
        counter = 0
        while await cls.filter(slug=slug).exists():
            counter += 1
            slug = f'{base_slug}-{counter}'
        avatar = cls(name=data.name, slug=slug, provider=data.provider, settings=data.settings, webhook = w)
        await avatar.save()
        return avatar
    
    async def update_avatar(self, data: AvatarPydantic, webhook: WebhookPydantic | None = None):
        if data.provider not in persona_link_providers:
            raise ValueError(f"Provider '{data.provider}' not found")
        
        provider = persona_link_providers[data.provider]
        if not provider.validate(data.settings):
            raise ValueError(f"Settings for provider '{data.provider}' are invalid")
        
        if webhook is not None:
            await self.fetch_related('webhook')
            await self.webhook.update_from_dict(webhook.model_bump())
            await self.webhook.save()
            
        self.name = data.name
        self.settings = data.settings
        await self.save()
        return self
    
    class Meta:
        table = "avatars"
        app = "persona_link"
    
