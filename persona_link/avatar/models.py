from enum import Enum
from typing import Optional

from pydantic import BaseModel
from tortoise import fields
from tortoise.models import Model

from persona_link.api_client import APIClient
from persona_link.persona_provider import persona_link_providers
from persona_link.persona_provider.models import AvatarType

ProviderEnum = Enum('ProviderEnum', {k:k for k in persona_link_providers.keys()})

class WebhookResponseData(BaseModel):
    """
    A class that represents the data to be sent to the webhook when a user speaks or messages from the frontend.
    
    Attributes:
        text (Optional[str]): Text spoken by the Avatar.
        media_url (Optional[str]): URL of the media file.
        media_type (Optional[AvatarType]): Type of the media file.
        conversation_id (str): ID that the source will use to determine conversation details.
    """
    text: Optional[str] = None
    media_url: Optional[str] = None
    media_type: Optional[AvatarType] = None
    conversation_id: str # id that the source will use to determining conversation details
    
class AvatarInput(BaseModel):
    """
    A class that represents the input to the Avatar from the application backend.
    
    Attributes:
        text (str): Text to be spoken by the Avatar.
        personalize (bool): Whether to personalize the Avatar.
    """
    text: str # text to speak
    personalize: bool = False # whether to personalize the avatar

class WebhookPydantic(BaseModel):
    """
    A pydantic model for the Webhook class for creating a webhook.
    
    Attributes:
        url (str): URL of the webhook.
        headers (dict): Headers for the webhook.
        method (str): Method of the webhook.
        get_text (bool): Whether to get text from the webhook.
        get_audio (bool): Whether to get audio from the webhook.
        get_video (bool): Whether to get video from the webhook.
        video_width (int): Width of the video.
        video_height (int): Height of the video.
        video_frame_rate (int): Frame rate of the video.
        audio_bit_rate (int): Bit rate of the audio.
        audio_sampling_rate (int): Sampling rate of the audio.
    """
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
    """
    A class to represent webhook in the database
    
    Attributes:
        id (int): Primary key for the Webhook, managed by the database.
        url (str): URL of the webhook.
        headers (dict): Headers for the webhook.
        method (str): Method of the webhook.
        get_text (bool): Whether to get text from the webhook.
        get_audio (bool): Whether to get audio from the webhook.
        get_video (bool): Whether to get video from the webhook.
        video_width (int): Width of the video.
        video_height (int): Height of the video.
        video_frame_rate (int): Frame rate of the video.
        audio_bit_rate (int): Bit rate of the audio.
        audio_sampling_rate (int): Sampling rate of the audio.
        created_at (Datetime): The time when the Webhook instance was created in the database.
        updated_at (Datetime): The time of the last update of the Webhook instance in the database. 
    """
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
    """
    A pydantic model for the Avatar class for creating an avatar.
    
    Attributes:
        name (str): Name for the Avatar.
        provider (str): Name of the registered provider ([persona_link.persona_provider.base.PersonaBase][]).
        settings (dict): Settings for the Avatar, specific the provider. The provider shall validate these settings.
    """
    name: Optional[str] = None
    provider: Optional[str] = None
    settings: Optional[dict] = None
    
class Avatar(Model):
    """
    A class that represents Avatar data in the database.

    Attributes:
        id (int): Primary key for the Avatar, managed by the database.
        name (str): Name for the Avatar.
        slug (str): Auto-generated unique identifier for the Avatar based upon the name.
        provider (str): Refers to a registered provider, [persona_link.persona_provider.base.PersonaBase][].
        settings (dict): Settings for the Avatar, specific the provider. The provider shall validate these settings.
        webhook (ForeignKey): Refers to implementation of: class:`persona_link.avatar.models.Webhook`.
            ForeignKey Webhook that the avatar is assigned to.
        created_at (Datetime):
            The time when the Avatar instance was created in the database.
        updated_at (Datetime):
            The time of the last update of the Avatar instance in the database. 
    """
    
    id = fields.IntField(pk=True, description="Primary Key")
    name = fields.CharField(255, description="Name for the avatar")
    slug = fields.CharField(255, unique=True, description="Auto-generated unique identifier")
    provider = fields.CharEnumField(ProviderEnum, description="Provider for the avatar") # for factory method
    settings = fields.JSONField(description="Settings for the avatar") # these settings will be validated by the provider
    webhook = fields.ForeignKeyField('persona_link.Webhook', related_name='avatars', description="Webhook to send the avatar to", null=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="Creation timestamp")
    updated_at = fields.DatetimeField(auto_now=True, description="Last update timestamp")
    
    def instance(self):
        return persona_link_providers[self.provider.value]()
    
    @classmethod
    async def create_avatar(cls, data: AvatarPydantic, webhook: WebhookPydantic | None = None):
        if not data.provider:
            raise ValueError("Provider not specified")
        
        if data.provider not in persona_link_providers:
            raise ValueError(f"Provider '{data.provider}' not found")
        
        provider = persona_link_providers[data.provider]
        if not provider.validate(data.settings):
            raise ValueError(f"Settings for provider '{data.provider}' are invalid")
        
        if not data.name:
            raise ValueError("Name not specified")
        
        if not data.settings:
            raise ValueError("Settings not specified")
        
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
        if data.provider and data.provider not in persona_link_providers:
            raise ValueError(f"Provider '{data.provider}' not found")
        
        provider = persona_link_providers[self.provider.value]
        if data.settings and not provider.validate(data.settings):
            raise ValueError(f"Settings for provider '{data.provider}' are invalid")
        
        if webhook is not None:
            await self.fetch_related('webhook')
            await self.webhook.update_from_dict(webhook.model_dump())
            await self.webhook.save()
            
        if data.name: 
            self.name = data.name
        if data.settings:
            self.settings = data.settings
        await self.save()
        return self
    
    class Meta:
        table = "avatars"
        app = "persona_link"
    
