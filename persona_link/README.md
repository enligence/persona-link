# Persona Link

Core library for all functionalities.

It is divided into four parts.

1. **Avatar**: This offers a consistent interface to create an avatar with any provider and also a database model to save created avatars.
2. **Persona Provider**: This contains all registered persona providers. As new providers are added, they get automatically registered and ready to use for Avatar creation. On of the personal providers, 'Sprite', uses only audio and renders the avatar in browser. **TTS** contains implementation of integrating various text to speech providers.
3. **Cache**: This offers storage and database layer to cache avatar responses in order to reuse them to avoid duplication, enhance performance and reduce costs.
4. **Personalization**: Offers ability to code methods to personalize. The key idea is to separation of concerns towards a performance and less expensive approach. One can think of adding custom pre / post message to the original message that the avatar is bound to speak. These extra messages can also be cached, reused and stitched together to give a personalized experience. 
