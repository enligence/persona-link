# Frontend Widgets for Persona Link

Interaction is 2-way and thus to offer full potential of the goals of this project, the project includes front-end widgets that connect to the persona-link server. Each widget must provide:
# React components for supporting interactive avatars

Persona link is a project where an AI agent can be linked to a persona. 
A persona is full duplex i.e. it can not only speak but also listen.

We have 2 types of personas

1. Video based like from HeyGen D-iD etc.
2. Audio based that will give audio and at least visemes (visual lip positions with timestamps)

In future we can add text based too for full set of features.

Any avatar component will connect with the backend api and get the avatar details for that id. The backend will be secured by ensuring that only allowed domains can request. The backend will give the necessary details like avatar type and other rendering related info e.g. whether it should collect user's video, audio or text. What should be the background etc. Whether interaction should be hands free, what gestures are allowed etc.

Based upon the avatar type it will load appropriate reach sub component, e.g. for a  video based avatar, it will simply be playing a video from a url. However for a audio based sprite avatar it will play the sprite images in sequence of the given visemes. If text has to be displayed too and highlighted as it is being spoken, then the work timestamps returned can also be used.

Based upon the settings, it will display text, record ot mic buttons. For hands free it will have appropriate UX and so on.

This components will play the avatar as the backend requests (connection via a web socket) at the same time it will stream, audio, video or text. For a hands free mode (only for audio/video), when there is a pause of 2 sec, we can assume that user is done speaking and avatar can respond. We can also do fancier things later, about using LLMs to determine context of whether user is done or not and have avatar respond with fillers like "hmm". "i see", "carry on" etc.

When user is done, the backend will either process the response or call a webhook for the calling app that is utilizing the avatar services. The app will have the logic to process the user's input and produce a response. It will ask the avatar to speak.