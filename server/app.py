"""
Example server to create and manage avatars. 
Actual implementation my involve more complex logic,
validation, security measures, and handling multiple tenants.
"""

from .settings import TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from .models import (
    ConnectedAvatar,
    AvatarListModel,
    Conversation,
    Message,
    Feedback,
    FeedbackPydantic,
    ConversationMessage,
    PersonaType,
    MessagePydantic,
    ConversationPydantic
)
from persona_link.avatar import speak, Avatar, AvatarInput
from persona_link.cache import Cache, AzureStorage, RelationalDB, md5hash
from persona_link.persona_provider.models import SpeakingAvatarInstance
from typing import List
from .ws import connections, router

app = FastAPI()

# add cors policy to allow localhost:3000 and localhost:8000
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = Cache(AzureStorage(), RelationalDB(), md5hash)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)


app.include_router(router, prefix="/ws")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

#################################################
# AVATAR Management Routes
#################################################
@app.get("/avatars/")
async def list_avatars() -> List[AvatarListModel]:
    avatars = await Avatar.all()
    return [
        AvatarListModel(name=avatar.name, slug=avatar.slug, provider=avatar.provider)
        for avatar in avatars
    ]


@app.put("/avatar/")
async def create_avatar(data: ConnectedAvatar):
    return await Avatar.create_avatar(data.avatar_settings, data.webhook_settings)


@app.post("/avatar/{avatar_slug}/")
async def update_avatar(avatar_slug: str, data: ConnectedAvatar):
    avatar = await Avatar.get_or_none(slug=avatar_slug)
    if avatar is None:
        raise ValueError(f"Avatar '{avatar_slug}' not found")
    print(data)
    avatar = await avatar.update_avatar(data.avatar_settings, data.webhook_settings)
    return avatar


@app.delete("/avatar/{avatar_slug}/")
async def delete_avatar(avatar_slug: str):
    avatar = await Avatar.get_or_none(slug=avatar_slug)
    if avatar is None:
        raise ValueError(f"Avatar '{avatar_slug}' not found")
    await avatar.delete()
    return {"status": "ok"}

#################################################
# AVATAR Interaction Routes
#################################################

@app.post("/avatar/{avatar_slug}/generate/")
async def avatarify(avatar_slug: str, input: AvatarInput) -> SpeakingAvatarInstance:
    return await speak(avatar_slug, cache, input)

@app.get("/conversation/{conversation_id}/messages/", response_model=List[MessagePydantic])
async def list_messages(conversation_id: str) -> List[MessagePydantic]:
    conversation = await Conversation.get_or_none(id=conversation_id)
    if conversation is None:
        return []
    messages = await Message.filter(conversation=conversation)
    return await MessagePydantic.from_queryset(messages)

@app.put("/conversation/{avatar_slug}/", response_model=ConversationPydantic)
async def create_conversation(avatar_slug: str) -> Conversation:
    from uuid import uuid4
    conversation_id = uuid4().hex
    conversation = await Conversation.create(conversation_id=conversation_id, avatar_slug=avatar_slug)
    return await ConversationPydantic.from_tortoise_orm(conversation)


@app.post("/conversation/{conversation_id}/")
async def converse(
    conversation_id: str, input: AvatarInput
) -> SpeakingAvatarInstance:
    websocket = connections.get(conversation_id, None)
    if websocket is None:
        raise ValueError(f"Conversation '{conversation_id}' has no active connection")
    
    conversation = await Conversation.get_or_none(id=conversation_id)
     
    if conversation is None:
        raise ValueError(f"Conversation '{conversation_id}' not found")
    
    speech: SpeakingAvatarInstance = await speak(conversation.avatar_slug, cache, input, conversation_id)
    
    message = await Message.create(
        conversation=conversation,
        persona_type=PersonaType.AGENT,
        text=input.text,
        media_url=speech.urls.media_url,
        visemes_url=speech.urls.visemes_url,
        word_timestamps_url=speech.urls.word_timestamps_url,
        metadata=speech.metadata,
        media_type=speech.avatar_type,
    )
    
    # get the number of existing messages in the conversation
    existing_messages_count = await ConversationMessage.filter(conversation=conversation).count()

    # create a new conversation message
    await ConversationMessage.create(
        conversation=conversation,
        message=message,
        order=existing_messages_count + 1,  # this will be the new order
    )
    
    # send the speech to websocket
    await websocket.send_json(message.dict())
    
@app.post("/feedback/{message_id}")
async def feedback(message_id: int, feedback: FeedbackPydantic):
    message = await Message.get_or_none(id=message_id)
    if message is None:
        raise ValueError(f"Message '{message_id}' not found")
    
    feedback_obj = await Feedback.get_or_none(message=message)
    if feedback_obj is None:
        # If Feedback for this message does not exist, create a new one
        feedback_obj = await Feedback.create(message=message, **feedback.dict())
    else:
        # If Feedback for this message exists, update it
        feedback_obj.feedback_thumb = feedback.feedback_thumb
        feedback_obj.feedback_text = feedback.feedback_text
        await feedback_obj.save()

    return feedback_obj
    


"""
Run as 
uvicorn server.app:app --port 9000 --reload

CREATE AVATAR:

curl -X 'PUT' \
  'http://localhost:9000/avatar/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "avatar_settings": {
    "name": "lisa",
    "provider": "Azure",
    "settings": {
        "voice":"en-IN-NeerjaNeural",
        "character":"lisa",
        "style":"graceful",
        "pose":"sitting",
        "video_format":"webm",
        "background_color":"#ffffff",
        "video_codec":"hevc"
    }
  },
  "webhook_settings": {
    "url": "https://localhost:8000/process",
    "headers": {},
    "method": "POST",
    "get_text": true,
    "get_audio": false,
    "get_video": false,
    "video_width": 320,
    "video_height": 240,
    "video_frame_rate": 25,
    "audio_bit_rate": 32,
    "audio_sampling_rate": 22050
  }
}'

# CREATE CONVERSATION

"""
