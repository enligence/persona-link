import json
from datetime import datetime
from persona_link.persona_provider.models import SpeakingAvatarInstance
from .models import (AvatarListModel, ConnectedAvatar, Conversation,
                     ConversationAvatar, ConversationMessage,
                     ConversationPydantic, Feedback, FeedbackPydantic, Message,
                     MessagePydantic, PersonaType)
from persona_link.avatar import Avatar, AvatarInput, get_avatar_info, speak
from persona_link.avatar.models import AvatarPydantic
from fastapi import FastAPI, WebSocket
from persona_link.cache import AzureStorage, Cache, RelationalDB, md5hash

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)
cache = Cache(AzureStorage(), RelationalDB(), md5hash)
async def construct_and_send(input: AvatarInput, websocket: WebSocket, conversation: Conversation):
    speech: SpeakingAvatarInstance = await speak(conversation.avatar_slug, cache, input)

    message = await Message.create(
        conversation=conversation,
        persona_type=PersonaType.AGENT,
        text=input.text,
        media_url=speech.urls.media_url,
        visemes_url=speech.urls.visemes_url,
        word_timestamps_url=speech.urls.word_timestamps_url,
        metadata=speech.metadata.model_dump(),
        media_type=speech.avatar_type,
    )

    # get the number of existing messages in the conversation
    existing_messages_count = await get_message_count(conversation)

    # create a new conversation message
    await ConversationMessage.create(
        conversation=conversation,
        message=message,
        order=existing_messages_count + 1,  # this will be the new order
    )


    message_pydantic = await MessagePydantic.from_tortoise_orm(message)
    message_json = json.dumps(message_pydantic.model_dump(), cls=DateTimeEncoder)
    
    await websocket.send_text(message_json)

async def get_message_count(conversation):
    existing_messages_count = await ConversationMessage.filter(
        conversation=conversation
    ).count()
    
    return existing_messages_count