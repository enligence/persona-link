import React, { useEffect, useState ,useRef} from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import SendIcon from '@material-ui/icons/Send';
import SendRoundedIcon from '@material-ui/icons/SendRounded';
function Avatarwidget(props) {
  const [isPlaying, setIsPlaying] = useState(false);
  const videoRef = useRef(null);
  const handlePlayVideo = () => {
    if (videoRef.current) {
      videoRef.current.play();
      setIsPlaying(true);
    }
  };

  const [ws, setWs] = useState(null);  
  const [messageData, setMessageData] = useState(null); 
  const [conversationId, setConversationId] = useState(props.conversationid);  // New state variable
  // setConversationId(props.conversationid)
// console.log(props.conversationid)
// console.log(props)
  const [inputValue, setInputValue] = useState(''); // Create state variable

  const handleInputChange = (event) => {
    setInputValue(event.target.value); // Update state variable with input value
  };
console.log('inputValue:', inputValue);
 
  // useEffect(() => {
  //   fetch('http://localhost:8000/create_conversation/')
  //     .then(response => response.json())
  //     .then(data => setConversationId(data.conversation_id));
    
  // }, []);
  console.log('conversationId:', conversationId);
  // console.log('avatr-alsug:', conversationId);
  // Connection
  useEffect(() => {
    if (conversationId) { 
    const websocket = new WebSocket(`ws://localhost:9000/ws/${conversationId}/`);
    setWs(websocket);
  }}, []);

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
  const buttonStyle = {
    padding: '10px 20px',
    marginLeft: '10px',
    border: 'none',
    backgroundColor: '#eee',
    cursor: 'pointer',
  };
  return (
//     <div>
//       <button onClick={handlePlayVideo} style={{ display: isPlaying ? 'none' : 'block' }}>
//         Play Initial Message
//       </button>
//      {messageData&&( <video
//         ref={videoRef}
//         src={messageData.media_url}
//         style={{ width: '50%', height: 'auto', display: isPlaying ? 'block' : 'none' }}
//       />)}
//     </div>
//   );
// }

// export default Avatarwidget;
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
       < button  onClick={handlePlayVideo} style={{  display: isPlaying ? 'none' : 'block' ,    padding: '10px 20px',
    marginLeft: '10px',
    border: 'none',
    backgroundColor: '#007bff',
    color: 'white',
    cursor: 'pointer',}}>
      Get Started
   </button>
      {messageData && (
        
      <video
        ref={videoRef}
        autoPlay  
        src={messageData.media_url}
       style={{ width: '50%', height: 'auto', display: isPlaying ? 'block' : 'none' }}
      />


          // {/* <video src={messageData.media_url} controls style={{ width: '50%', height: 'auto' }} /> */}
          // {/* <video src={messageData.media_url}  autoPlay style={{ width: '50%', height: 'auto' }} /> */}
          // {/* <video src={messageData.media_url}  autoPlay  controls style={{ width: '50%', height: 'auto' }} /> */}
      )}
 <Box ref={videoRef}
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '25ch' },
      }}
      noValidate
      autoComplete="off"
      
    ><div style={{ display: 'flex', alignItems: 'center' ,display: isPlaying ? 'block' : 'none'}}>
      <TextField id="outlined-basic" label="Enter a message " variant="outlined" value={inputValue} 
      onChange={handleInputChange}   >  </TextField><SendRoundedIcon color="primary" onClick={() => sendMessage(inputValue)} style={{marginLeft:"10px",marginTop: '10px' , marginRight: '10px' }}fontSize="large"></SendRoundedIcon>
  </div>
    </Box>
    

    </div>
  );
}

export default Avatarwidget;
