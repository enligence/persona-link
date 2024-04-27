from pydantic import BaseModel

class Personalization(BaseModel):
    prefix: str = None
    suffix: str = None