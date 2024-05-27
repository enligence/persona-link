An example application and basic server features for using persona_link

## Running

1. [Install poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
2. Ensure you have python 3.10 and above.
4. clone this repository and cd to it.
3. create virtual env `python3 -m venv .venv`
4. activate the env `source .venv/bin/activate`
5. run `poetry install` to install the dependencies
6. create your `.env` file based upon the `.env.example`
7. run the server `uvicorn server.app:app --port 9000 --reload`
8. run teh example application `uvicorn server.example:app --port 8000 --reload`
9. run frontend example `npm start`


## Setting the DB

Current support is for relational databases using [Tortoise ORM](https://tortoise.github.io/)
After setting the `DB_URL` env var in `.env`, run:

```
aerich init -t server.settings.TORTOISE_ORM
aerich init-db
```

The above is only for the first time. After any new updates simply do

```
aerich migrate
```