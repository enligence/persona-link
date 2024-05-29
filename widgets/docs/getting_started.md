# React Widget

## Installation

To install the widget, do the following:

1. `npm i persona-link-avatar --force`
2. Before using the avatar-widget please make sure that your backend example server must be serving on 8000 port
3. After that import the widget into your React component: `import Avatarwidget from 'persona-link-avatar';`
4. Then, you can use it in your component's render method like:

```
function name() {
  return (

     
      {conversationId&&( <Avatarwidget conversationid= {conversationId} websocketadd="localhost:9000" />)}
   
  );
}
```