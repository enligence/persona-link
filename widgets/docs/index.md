# Persona Link Frontend Widgets

This project aims to provide interactive avatars that connect to the Persona Link server. Each widget is designed to offer a full duplex interaction, where the AI agent, linked to a persona, can listen and respond according to the mode set.

We provide frontend widgets for avatars that support:

- Video mode, e.g., from HeyGen, D-id, Azure etc.
- Sprite-based mode, where the avatar delivers audio and displays visemes (visual lip positions with timestamps)
- Audio mode, where the avatar only plays its audio

A text-based mode might be introduced in the future for a full set of interactive features.

## Connecting to Back-end

Each avatar component connects with the backend API and fetches avatar details using the unique ID. The back-end will give rendering-related instructions like the avatar type, whether it should collect user's video, audio, or text, the type of background, and also the nature and type of interaction.

## Avatar Rendering

Based on the avatar type, the component will load the appropriate react sub-component. For a video avatar, the component will play the video from a given URL. For an audio-based sprite avatar, it will sequence the sprite images based on the returned visemes timestamps. If text has to be displayed and highlighted as it is spoken, the accompanying word timestamps can be used.

## Interactive features

The component will use various settings to display, record, or send mic buttons. For hands-free UX, it will offer gesture-based interaction and other features like a pause of 2 sec to indicate the user has ended speaking and it's avatar's turn to reply.

The backend will process the user’s response or trigger a webhook for the calling app that utilizes the avatar services. The app will contain the logic to process user's input and generate a response, which will then be delivered by the avatar.

## Contributing

We welcome contributions of all sorts to Persona Link. Whether you're improving documentation, adding new features or simply reporting bugs, remember, any contribution can make a significant impact.

## Installation and Usage

Check [getting_started](getting_started.md) for the setup guide.

## License 

This project is licensed under [MIT](LICENSE).