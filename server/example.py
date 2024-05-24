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

