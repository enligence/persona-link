from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from persona_link.avatar import call_webhook
from persona_link.avatar.models import Avatar, AvatarInput, WebhookResponseData


from .models import Conversation

router = APIRouter()

connections: dict[str, WebSocket] = {}


@router.websocket("/{conversation_id}/")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    from .app import construct_and_send, get_message_count
    """
    This endpoint is used to establish a websocket connection for a conversation.

    route: `/ws/{conversation_id}`
    method: WebSocket

    Parameters:
        websocket (WebSocket): The websocket connection
        conversation_id (str): The ID of the conversation
    """
    print(conversation_id)
    await websocket.accept()
    

    # if conversation_id in connections:
    #     # If there is already a connection for this conversation_id, close it
    #     await connections[conversation_id].close()

    conversation = await Conversation.get_or_none(conversation_id=conversation_id)
    if conversation is None:
        # close this connection after sending the error message and remove from the connections
        await websocket.send_text("Conversation not found")
        await websocket.close()
    else:
        print(conversation.avatar_slug)
        avatar = await Avatar.get_or_none(slug=conversation.avatar_slug)
        print(avatar)
        if avatar.initial_message:
            existing_messages_count = await get_message_count(conversation=conversation)
            # if existing_messages_count == 0:  # only send the first time
            await construct_and_send(
                    AvatarInput(text=avatar.initial_message), websocket, conversation
                )

        # Store the websocket connection
        connections[conversation_id] = websocket

        # TODO: if there is initial_message, send over websocket now.

        try:
            while True:
                data = await websocket.receive_text()

                # call webhook of conversation's configured avatar
                webhook_data = WebhookResponseData(
                    text=data, conversation_id=conversation_id
                )

                await call_webhook(conversation.avatar_slug, webhook_data)

        except WebSocketDisconnect:
            # Remove the disconnected connection
            del connections[conversation_id]
# async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
#     print(conversation_id)
#     await websocket.accept()
    
#     # if conversation_id in connections:
#     #     # If there is already a connection for this conversation_id, close it
#     #     print("disconnected")
#     #     await connections[conversation_id].close()
        
#     # Store the websocket connection
#     connections[conversation_id] = websocket

#     try:
#         while True:
#             data = await websocket.receive_text()
#             conversation = await Conversation.get_or_none(conversation_id=conversation_id)
#             print(conversation)
#             if conversation is None:
#                 # close this connection after sending the error message and remove from the connections
#                 await websocket.send_text("Conversation not found")
#                 del connections[conversation_id]
#                 await websocket.close()
#                 break
            
#             # call webhook of conversation's configured avatar
#             webhook_data = WebhookResponseData(
#                 text=data,
#                 conversation_id=conversation_id
#             )
            
#             await call_webhook(conversation.avatar_slug, webhook_data)


#     except WebSocketDisconnect:
#         pass
#         # Remove the disconnected connection
#         # # print("disconnected")
#         if conversation_id in connections:
#             del connections[conversation_id]
            
