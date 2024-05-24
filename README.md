# Persona Link
This new open source project intends to revolutionize the digital human industry by making it easier for users to integrate their AI-based agents with any avatar or digital human provider. 

The main features of the project include:
1. **Interoperability**: Our solution provides a standard interface that allows users to seamlessly integrate any AI-based agent with any avatar or digital human provider.
2. **Caching**: We also offer a caching layer that significantly improves performance by storing recurring similar requests and their responses. This means that the system won't have to exert extra computational efforts to process the similar requests from scratch.
3. **Personalization**: In addition, our product has a personalization layer that allows users to customize their avatars or digital humans based on specific preferences or requirements.
4. **Front-end Widgets**: Lastly, we plan to offer front-end widgets that users can incorporate into their websites or applications. These widgets will offer a host of features that will further enhance the user experience.

As an open-source product, our project is built by the community for the community. We're looking for developers, designers, and anyone interested in digital humans and AI to contribute to this exciting project. 

With your help, we can transform the world of digital humans and create a unique, engaging, and immersive user experience. Please join us as we usher in a new era in digital human technology. Let's make the digital world more interactive and enjoyable.

## Our Goals

* **Innovation**: We aim to revolutionize the digital human industry by offering a unique platform which integrates AI and digital humans.
* **Community**: Encourage cooperation and assistance from developers, designers, and anyone with an interest in advancing AI and digital human technology.
* **User-Centered**: Propel the industry forward by creating a platform based on the needs of the users, making digital human interaction a seamless experience.
* **Transparency**: Foster an open-source community where development is done in plain sight, offering clarity and trust to the users.

## Getting Started

Follow the instructions to get a copy of this project up and running on your local machine for development and testing purposes.

### Prerequisites 

A list of technologies that you need to have installed and how to install them

### Installation 

A step by step series of commands and procedures that tells you how to set up your local environment.

## How to Contribute

We greatly appreciate any contribution to Persona Link. It's our contributors who help make this project better and more beneficial for everyone. Check out our `CONTRIBUTING` file to find out how you can be a part of this incredible project.

## Code of Conduct

Outlines how contributors should interact with each other. Please read and follow our `CODE_OF_CONDUCT` to maintain a positive and inclusive environment.

## Licensing 

This project leverages an open source license. For more details, please check out the `LICENSE` file.

## Contact Information

If you have any questions, comments, or concerns, feel free to contact us. We are open to feedback and are always excited to discuss new ideas!

---

By contributing to Persona Link, you're helping shape the future of digital human technology. Together, we can create new connections, new experiences, and ultimately, a new world.

Thank you for your interest in Persona Link. We can't wait to build the future with you!

```
poetry install --with server,azure,postgres,local-storage,dev,test

First time:
aerich init -t server.settings.TORTOISE_ORM
aerich init-db 

Then onwords for any model changes
aerich migrate
```