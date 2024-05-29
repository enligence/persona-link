"""
Example server to create and manage avatars. 
Actual implementation my involve more complex logic,
validation, security measures, and handling multiple tenants.
"""

from typing import List

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from persona_link.avatar import Avatar, AvatarInput, get_avatar_info, speak
from persona_link.avatar.models import AvatarPydantic
from persona_link.cache import AzureStorage, Cache, RelationalDB, md5hash
from persona_link.persona_provider.models import SpeakingAvatarInstance

from .models import (AvatarListModel, ConnectedAvatar, Conversation,
                     ConversationAvatar, ConversationMessage,
                     ConversationPydantic, Feedback, FeedbackPydantic, Message,
                     MessagePydantic, PersonaType)
from .settings import TORTOISE_ORM
from .ws import connections, router

app = FastAPI()

# add cors policy to allow localhost:3000 and localhost:8000

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
    """
    List all the avatars

    route : `/avatars/`
    method: GET

    Returns:
    List[ AvatarListModel ]: List of all avatars [server.models.AvatarListModel][]
    """
    avatars = await Avatar.all()
    return [
        AvatarListModel(name=avatar.name, slug=avatar.slug, provider=avatar.provider)
        for avatar in avatars
    ]


@app.put("/avatar/")
async def create_avatar(data: ConnectedAvatar) -> AvatarPydantic:
    """
    Create a new avatar

    route: `/avatar/`
    method: PUT

    Parameters:
        data (ConnectedAvatar): The data for the new avatar

    Returns:
        Avatar: The created avatar
    """
    avatar = await Avatar.create_avatar(
        data.avatar_settings, data.webhook_settings, data.initial_message
    )
    return AvatarPydantic(
        name=avatar.name,
        provider=avatar.provider,
        settings=avatar.settings,
    )


@app.post("/avatar/{avatar_slug}/")
async def update_avatar(avatar_slug: str, data: ConnectedAvatar) -> AvatarPydantic:
    """
    Update the avatar with the given slug

    route: `/avatar/{avatar_slug}/`
    method: POST

    Parameters:
        avatar_slug (str): The slug of the avatar to update
        data (ConnectedAvatar): The updated data for the avatar

    Returns:
        Avatar: The updated avatar
    """
    avatar = await Avatar.get_or_none(slug=avatar_slug)
    if avatar is None:
        raise ValueError(f"Avatar '{avatar_slug}' not found")

    avatar = await avatar.update_avatar(
        data.avatar_settings, data.webhook_settings, data.initial_message
    )
    return AvatarPydantic(
        name=avatar.name,
        provider=avatar.provider,
        settings=avatar.settings,
    )


@app.delete("/avatar/{avatar_slug}/")
async def delete_avatar(avatar_slug: str) -> dict:
    """
    Delete the avatar with the given slug

    route: `/avatar/{avatar_slug}/`
    method: DELETE

    Parameters:
        avatar_slug (str): The slug of the avatar to delete

    Returns:
        dict: The status of the deletion
    """
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
    """
    Generate the avatar for the given input

    route: `/avatar/{avatar_slug}/generate/`
    method: POST

    Parameters:
        avatar_slug (str): The slug of the avatar to use
        input (AvatarInput): The input text to speak

    Returns:
        SpeakingAvatarInstance: The instance of the speaking avatar
    """
    return await speak(avatar_slug, cache, input)


@app.get(
    "/conversation/{conversation_id}/messages/", response_model=List[MessagePydantic]
)
async def list_messages(conversation_id: str) -> List[MessagePydantic]:
    """
    List all the messages in the conversation

    route: `/conversation/{conversation_id}/messages/`
    method: GET

    Parameters:
        conversation_id (str): The ID of the conversation

    Returns:
        List[ MessagePydantic ]: List of all messages in the conversation
    """
    conversation = await Conversation.get_or_none(id=conversation_id)
    if conversation is None:
        return []
    messages = await Message.filter(conversation=conversation)
    return await MessagePydantic.from_queryset(messages)


@app.put("/conversation/{avatar_slug}/", response_model=ConversationPydantic)
async def create_conversation(avatar_slug: str) -> Conversation:
    """
    Create a new conversation

    route: `/conversation/{avatar_slug}/`
    method: PUT

    Parameters:
        avatar_slug (str): The slug of the avatar to use

    Returns:
        Conversation: The created conversation
    """
    from uuid import uuid4

    conversation_id = uuid4().hex
    conversation = await Conversation.create(
        conversation_id=conversation_id, avatar_slug=avatar_slug
    )
    return await ConversationPydantic.from_tortoise_orm(conversation)


@app.get("/conversation/{conversation_id}/", response_model=ConversationAvatar)
async def get_conversation_avatar(conversation_id: str) -> ConversationAvatar:
    """
    Get the avatar for the conversation

    route: `/conversation/{conversation_id}/`
    method: GET

    Parameters:
        conversation_id (str): The ID of the conversation

    Returns:
        ConversationAvatar: The avatar for the conversation
    """
    conversation = await Conversation.get_or_none(conversation_id=conversation_id)
    if conversation is None:
        raise ValueError("Conversation not found")

    avatar, avatar_type = await get_avatar_info(conversation.avatar_slug)

    return ConversationAvatar(
        avatar_type=avatar_type,
        avatar_slug=conversation.avatar_slug,
        avatar_name=avatar.name,
        avatar_provider_name=avatar.provider,
    )


@app.post("/conversation/{conversation_id}/")
async def converse(conversation_id: str, input: AvatarInput):
    """
    Converse in the conversation.
    This will speak the input text and send it to the conversation websocket connection

    route: `/conversation/{conversation_id}/`
    method: POST

    Parameters:
        conversation_id (str): The ID of the conversation
        input (AvatarInput): The input text to speak
    """
    websocket = connections.get(conversation_id, None)
    if websocket is None:
        raise ValueError(f"Conversation '{conversation_id}' has no active connection")

    conversation = await Conversation.get_or_none(conversation_id=conversation_id)

    if conversation is None:
        raise ValueError(f"Conversation '{conversation_id}' not found")

    await construct_and_send(input, websocket, conversation)

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
    # send the speech to websocket
    await websocket.send_json(message_pydantic.model_dump())

async def get_message_count(conversation):
    existing_messages_count = await ConversationMessage.filter(
        conversation=conversation
    ).count()
    
    return existing_messages_count


@app.post("/feedback/{message_id}")
async def feedback(message_id: int, feedback: FeedbackPydantic) -> FeedbackPydantic:
    """
    Provide feedback for the message

    route: `/feedback/{message_id}`
    method: POST

    Parameters:
        message_id (int): The ID of the message
        feedback (FeedbackPydantic): The feedback data

    Returns:
        Feedback: The feedback object
    """
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

    return FeedbackPydantic(
        feedback_thumb=feedback_obj.feedback_thumb,
        feedback_text=feedback_obj.feedback_text,
    )


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
        "video_format":"mp4",
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
