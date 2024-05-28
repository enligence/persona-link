from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from persona_link.avatar import AvatarPydantic, WebhookPydantic
from persona_link.persona_provider.models import AvatarType


class ConnectedAvatar(BaseModel):
    """
    Model for an Avatar connected to the application backend using a webhook
    
    Attributes:
        avatar_settings (Optional[AvatarPydantic]): Settings of the Avatar. Defaults to None.
        webhook_settings (Optional[WebhookPydantic]): Settings of the Webhook. Defaults to None.
        initial_message (Optional[str]): Initial message for Avatar to speak. Defaults to None.
    """
    avatar_settings: Optional[AvatarPydantic] = None
    webhook_settings: Optional[WebhookPydantic] = None
    initial_message: Optional[str] = None
    
class AvatarListModel(BaseModel):
    """
    Class for a single Avatar in the list of Avatars when returned in bulk
    
    Attributes:
        name (str): Name of the Avatar
        slug (str): Slug of the Avatar
        provider (str): Provider of the Avatar
    """
    name: str
    slug: str
    provider: str
    
class PersonaType(Enum):
    """
    Enum for the type of persona
    
    Attributes:
        AGENT (str): Agent persona
        HUMAN (str): Human persona
    """
    AGENT = "agent"
    HUMAN = "human"

class Message(Model):
    """
    Model for a message
    
    Attributes:
        id (int): Primary Key
        persona_type (PersonaType): Type of persona
        text (str): text of message
        media_url (str): media url or audio or video
        visemes_url (str): visemes url from agent
        word_timestamps_url (str): word timestamps url from agent
        metadata (dict): metadata for the message
        media_type (AvatarType): type of media
        created_at (datetime): Creation timestamp
    """
    id = fields.IntField(pk=True, description="Primary Key")
    persona_type = fields.CharEnumField(PersonaType, description="Type of persona")

    text = fields.TextField(description="text of message", null=True)
    media_url = fields.CharField(255, description="media url or audio or video", null=True)
    visemes_url = fields.CharField(255, description="visemes url from agent", null=True)
    word_timestamps_url = fields.CharField(255, description="word timestamps url from agent", null=True)
    metadata = fields.JSONField(description="metadata for the message", null=True)
    media_type = fields.CharEnumField(AvatarType, description="type of media", null=True)

    created_at = fields.DatetimeField(auto_now_add=True, description="Creation timestamp")

    class Meta:
        table = "messages"

class MessagePydantic(pydantic_model_creator(Message, name="MessagePydantic")):
    """
    Pydantic model for a message
    
    Attributes:
        persona_type (PersonaType): Type of persona
        text (str): text of message
        media_url (str): media url or audio or video
        visemes_url (str): visemes url from agent
        word_timestamps_url (str): word timestamps url from agent
        metadata (dict): metadata for the message
        media_type (AvatarType): type of media
        created_at (datetime): Creation timestamp
    """
    model_config = ConfigDict(from_attributes=True)

class Feedback(Model):
    """
    Model for feedback on a message ( [server.models.Message][] )
    
    Attributes:
        message (fields.ForeignKeyField): Message for which feedback is given
        feedback_thumb (fields.BooleanField): thumbs up(true) or thumbs down(false) for the interaction
        feedback_text (fields.TextField): detailed feedback on the interaction
        updated_at (fields.DatetimeField): Last update timestamp
    """
    message = fields.ForeignKeyField('models.Message', related_name='feedback', on_delete=fields.CASCADE, description="Message for which feedback is given", unique=True)
    
    feedback_thumb = fields.BooleanField(description="thumbs up(true) or thumbs down(false) for the interaction", null=True)
    feedback_text = fields.TextField(description="detailed feedback on the interaction", null=True)

    updated_at = fields.DatetimeField(auto_now=True, description="Last update timestamp")
    
    class Meta:
        table = "feedbacks"
        
class FeedbackPydantic(BaseModel):
    """
    Pydantic model for feedback on a message for API
    
    Attributes:
        feedback_thumb (bool): thumbs up(true) or thumbs down(false) for the interaction
        feedback_text (str): detailed feedback on the interaction
    """
    model_config = ConfigDict(from_attributes=True)
    
    feedback_thumb: bool
    feedback_text: str
    
class Conversation(Model):
    """
    Model for a conversation
    
    Attributes:
        id (int): Primary Key
        conversation_id (str): Conversation id
        avatar_slug (str): Avatar slug
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    """
    id = fields.IntField(pk=True, description="Primary Key")
    conversation_id = fields.CharField(255, description="Conversation id", unique=True)
    avatar_slug = fields.CharField(255, description="Avatar slug")
    created_at = fields.DatetimeField(auto_now_add=True, description="Creation timestamp")
    updated_at = fields.DatetimeField(auto_now=True, description="Last update timestamp")
    
    class Meta:
        table = "conversations"
        
class ConversationPydantic(pydantic_model_creator(Conversation, name="ConversationPydanticIn", exclude_readonly=True)):
    model_config = ConfigDict(from_attributes=True)
    
class ConversationAvatar(BaseModel):
    """
    Model for the avatar in a conversation
    
    Attributes:
        avatar_type (AvatarType): Type of avatar
        avatar_slug (str): Avatar slug
        avatar_name (str): Avatar name
        avatar_provider_name (str): Avatar provider name
    """
    avatar_type: AvatarType
    avatar_slug: str
    avatar_name: str
    avatar_provider_name: str
        
class ConversationMessage(Model):
    """
    Model for a message in a conversation
    
    Attributes:
        id (int): Primary Key
        conversation (fields.ForeignKeyField): Conversation to which the message belongs
        message (fields.ForeignKeyField): Message in the conversation
        order (int): Order in which messages appear in the conversation
    """
    id = fields.IntField(pk=True, description="Primary Key")
    conversation = fields.ForeignKeyField('models.Conversation', related_name='messages', on_delete='CASCADE')
    message = fields.ForeignKeyField('models.Message', related_name='conversations', on_delete='CASCADE')
    order = fields.IntField(description="Order in which messages appear in the conversation")

    class Meta:
        table = "conversation_messages"