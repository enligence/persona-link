"""
A client app wants to use persona_link for avatar use.
The client backend server will have a persona_link server running or connect to a managed persona_link server.
The client frontend will include persona_link react components to interact with the persona_link websocket server.

The workflow is as follows:
1. client creates and account (if managed) on persona link and gets an API_KEY
2. The client configures an avatar in persona_link after logging in.
3. The client gets the unique avatar slug.
4. On client app when their user logs in for some conversation, the client backend procures a conversation_id for the created avatar. Client backend may have stored a previous conversation id or they can request a new one.
5. On client frontend it provides the conversation_id
6. the frontend fetches details from the personal_link server 
7. The frontend have capability to tecord user's message (text, audio or video) and send it to the persona_link server over secure websocket.
8. The backend server can send text to speak to the persona_link server
9. if frontend sends user's message, persona link calls the webhook of the client backend server with the message details
10. The client backend can process or intiate and call api endpoint of persona link to respond. personal link will find the websocket associated and generate the appropriate avatar info to play on the frontend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from persona_link import APIClient
from persona_link.avatar.models import AvatarInput, WebhookResponseData

app = FastAPI()
import requests
import json
# add cors policy to allow localhost:3000 and localhost:9000
def init_avatar():
    url = 'http://localhost:9000/avatar/'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
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
            "url": "http://localhost:8000/process/",
            "headers": {},
            "method": "POST",
            "get_text": True,
            "get_audio": False,
            "get_video": False,
            "video_width": 320,
            "video_height": 240,
            "video_frame_rate": 25,
            "audio_bit_rate": 32,
            "audio_sampling_rate": 22050
        },
        "initial_message": "Hello, I am Lisa. How can I help you?"
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    return response.json()

# Call the function

response= requests.get('http://localhost:9000/avatars/')
if len(response.json()) ==0:
    init_avatar()

    


# print(init_avatar())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:9000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

avatar_slug = "lisa"

@app.get("/create_conversation/")
async def create_conversation():
    "the app may want to stor it and reuse it for the same user"
    return await APIClient().put_request(f"http://localhost:9000/conversation/{avatar_slug}/")

@app.post("/process/")
async def process(data: WebhookResponseData):
    # process the data
    # for now this is a test only
    #print(data)
    # we shall now ask the persona_link server to say the sme thing i.e. an echo bot
    input = AvatarInput(
        text=data.text,
        personalize=False
    )
    await APIClient().post_request(f"http://localhost:9000/conversation/{data.conversation_id}/", payload=input.model_dump())