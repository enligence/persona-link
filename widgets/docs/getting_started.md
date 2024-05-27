# My React Widget

## Installation

To install the widget, use the following command:

step1:
npm i avatar-widgets


step2:
 before using th avatar-widget please make sure that ypur backend example server  must be serving on 8000 port


step3:
 after that import the widget into your React component:
as 

import Avatarwidget from 'avatar-widgets';


step4:

Then, you can use it in your component's render method like so:


example:

""
Here message a prop where you send a conversation message to widget then widget can send this to the sever 
""

render() {
  return (

      <Avatarwidget message="nice to meet you mr. john" />
   
  );
}