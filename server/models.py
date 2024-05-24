from persona_link.avatar import AvatarPydantic, WebhookPydantic
from persona_link.persona_provider.models import AvatarType
from pydantic import BaseModel, ConfigDict
from typing import Optional
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


from enum import Enum

class ConnectedAvatar(BaseModel):
    avatar_settings: Optional[AvatarPydantic] = None
    webhook_settings: Optional[WebhookPydantic] = None
    
class AvatarListModel(BaseModel):
    name: str
    slug: str
    provider: str
    
class PersonaType(Enum):
    AGENT = "agent"
    HUMAN = "human"

class Message(Model):
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
    model_config = ConfigDict(from_attributes=True)

class Feedback(Model):
    message = fields.ForeignKeyField('models.Message', related_name='feedback', on_delete=fields.CASCADE, description="Message for which feedback is given", unique=True)
    
    feedback_thumb = fields.BooleanField(description="thumbs up(true) or thumbs down(false) for the interaction", null=True)
    feedback_text = fields.TextField(description="detailed feedback on the interaction", null=True)

    updated_at = fields.DatetimeField(auto_now=True, description="Last update timestamp")
    
    class Meta:
        table = "feedbacks"
        
class FeedbackPydantic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    feedback_thumb: bool
    feedback_text: str
    
class Conversation(Model):
    id = fields.IntField(pk=True, description="Primary Key")
    conversation_id = fields.CharField(255, description="Conversation id", unique=True)
    avatar_slug = fields.CharField(255, description="Avatar slug")
    created_at = fields.DatetimeField(auto_now_add=True, description="Creation timestamp")
    updated_at = fields.DatetimeField(auto_now=True, description="Last update timestamp")
    
    class Meta:
        table = "conversations"
        
class ConversationPydantic(pydantic_model_creator(Conversation, name="ConversationPydanticIn", exclude_readonly=True)):
    model_config = ConfigDict(from_attributes=True)
        
class ConversationMessage(Model):
    id = fields.IntField(pk=True, description="Primary Key")
    conversation = fields.ForeignKeyField('models.Conversation', related_name='messages', on_delete='CASCADE')
    message = fields.ForeignKeyField('models.Message', related_name='conversations', on_delete='CASCADE')
    order = fields.IntField(description="Order in which messages appear in the conversation")

    class Meta:
        table = "conversation_messages"