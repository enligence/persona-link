# Getting Started

You can either clone and run the server locally and connect your application, or directly use the [persona link library](/Library/getting_started/) by connecting your chat routes appropriately. 

This server and example will offer basic guidelines.

## Running the server

Assuming:

* a virtual env is created and you have done `poetry install` so all necessary dependencies are present.
* you are in persona_link folder (parent to the server folder).
* a `.env` is created as per `.env.example` filling all detains of providers you intend to use.


> Run server
```
uvicorn server.app:app --port 9000 --reload
```
> Run example application
```
uvicorn server.example:app --port 8000 --reload
```

> Run the frontend example
```
To Be Filled
```

Now open `http://localhost:3000` in a browser and try it out!

