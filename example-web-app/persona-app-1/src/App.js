import './App.css';
import Avatarwidget from 'persona-link-avatar';
import React, { useEffect, useState } from 'react';

import img1 from './image 94 (1).png';
import img2 from './image 94 (2).png';
import img3 from './image 94 (3).png';
import img4 from './image 94.png';
function App() {
  // conversationid
  const [conversationId, setConversationId] = useState("");
  useEffect(() => {
    fetch(`http://localhost:8000/create_conversation/`)
      .then(response => response.json())
      .then(data => setConversationId(data.conversation_id));

  }, []);
  console.log('conversation__Id:', conversationId);
  console.log('avatr---alsug:', conversationId);
  return (
    <div className="App">
      <nav className="navbar">
        <div className="navbar__logo">Persona-link</div>
        <div className="navbar__links">
          <a href="#">How it works</a>
          <a href="#">See examples</a>
          <a href="#">Pricing</a>
          <a href="#">FAQ</a>
          <button className="navbar__button">Log in</button>
          <button className="navbar__button navbar__button--primary">Sign up</button>
        </div>
      </nav>
      <header className="App-header">

        {
          conversationId && (
            <Avatarwidget conversationid={conversationId} websocketadd="localhost:9000" />
          )
        }

      </header>
      <section className="examples">
        <h2>Examples of AI avatars</h2>
        <div className="examples__grid">
          <img src={img1} alt="Example 1" />
          <img src={img2} alt="Example 2" />
          <img src={img3} alt="Example 3" />
          <img src={img4} alt="Example 4" />
        </div>
        <button className="examples__button">Create Your Avatar</button>
      </section>
    </div>
  );
}

export default App;
