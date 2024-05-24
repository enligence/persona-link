import os

from dotenv import load_dotenv

load_dotenv()

TORTOISE_ORM = {
    "connections": {"default": os.getenv("DB_URL")},
    "apps": {
        "models": {
            "models": ["server.models", "aerich.models"],
            "default_connection": "default",
        },
        "persona_link": {
            "models": ["persona_link.avatar.models"],
            "default_connection": "default",
        }
    },
}