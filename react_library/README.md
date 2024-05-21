# React components for supporting interactive avatars

Persona link is a project where an AI agent can-be linked to a persona. 
A persona is bi-modal i.e. it can not only speak but also listen.

We have 2 types of personas

1. Video based like from HeyGen D-iD etc. <- expensive
2. Audio based that will give audio and at least visemes (visual lyp positions with timestamps) <- a lot cheaper

Currently we have 6 Skill2030 avatars and we need a way to create more of them. We definitely need to develop complete workflow to take any head-shot of a real or virtual character and create 21 viseme sprites as mentioned on [Azure Visemes Page]
(https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-speech-synthesis-viseme?tabs=visemeid&pivots=programming-language-python).

Given that the python package - Avatar is almost done, we need to start working on the Web App and a demo part.

Before that we need to complete the react library. It will have a single component that will dynamically load either video avatar parts or audio avatar parts.

<avatar id="avatar_id" api_endpoint="https://..."... some other settings></avatar> or how ever it works in React!

avatar component will connect with the backend api and get the avatar details for that id. The backend will be secured by ensuring that only allowed domains can request. The backend will give the necessary details like avatar type and other rendering related info e.g. whether it should collect user's video, audio or text. What should be the background etc. Whether interaction should be hands free, what gestures are allowed etc.

Based upon the avatar type it will load appropriate reach sub component, e.g. for a  video based avatar, it will simply be playing a video from a url. However for a audio based sprite avatar it will play the sprite images in sequence of the given visemes. If text has to be displayed too and highlighted as it is being spoken, then the work timestamps returned can also be used.

Based upon the settings, it will display text, record ot mic buttons. For hands free it will have appropriate UX and so on.

This components will play the avatar as the backend requests (connection via a web socket) at the same time it will stream, audio, video or text. For a hands free mode (only for audio/video), when there is a pause of 2 sec, we can assume that user is done speaking and avatar can respond. We can also do fancier things later, about using LLMs to determine context of whether user is done or not and have avatar respond with fillers like "hmm". "i see", "carry on" etc.

When user is done, the backend will either process the response or call a webhook for the calling app that is utilizing the avatar services. The app will have the logic to process the user's input and produce a response. It will ask the avatar to speak.

---
Given above workflow we need to then create a web application for the same. The application must have sign-in / sign-up as usual (supertokens can be used for that) and some monetization logic (yet to decide). And one can create an avatar or edit existing avatar. Pick avatar type (video / sprite) and configure each appropriately. This avatar will be stored with a avatarid in the database. For each avatar configures, the user will also provide webhook to call

We need to create a basic demo of using this. Then release the opensource project and the corresponding managed paid webapp.

In future, we can add RAG and auto chat features for simpler chat use cases.

