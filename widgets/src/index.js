import React, { useEffect, useState } from 'react';

function Avatarwidget(props) {
  const [ws, setWs] = useState(null);  
  const [messageData, setMessageData] = useState(null); 
  const [conversationId, setConversationId] = useState(null);  // New state variable 
  const [userMessage, setUserMessage] = useState(props.message);
  useEffect(() => {
    fetch('http://localhost:8000/create_conversation/')
      .then(response => response.json())
      .then(data => setConversationId(data.conversation_id));
    
  }, []);
  console.log('conversationId:', conversationId);
  console.log('avatr-alsug:', conversationId);
  // Connection
  useEffect(() => {
    if (conversationId) { 
    const websocket = new WebSocket(`ws://localhost:9000/ws/${conversationId}/`);
    setWs(websocket);
  }}, [conversationId]);

  // Message handling
  useEffect(() => {
    if (ws) {
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Received data:', data);
        setMessageData(data);
      };
      ws.onclose = () => {
        console.log('WebSocket connection closed');
      };
    }
  }, [ws]);

  // Sending a message
  const sendMessage = (message) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(message);

    } else {
      console.error('Cannot send message: WebSocket is not open');
    }
  };

  return (
    <div>
      <button onClick={() => sendMessage(userMessage)}>Send Message</button>
      {messageData && (
        <div>
  
          <video src={messageData.media_url} controls style={{ width: '50%', height: 'auto' }} />
        </div>
      )}
    </div>
  );
}

export default Avatarwidget;
