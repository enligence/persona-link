from typing import AsyncGenerator, List, Optional
from pydantic import BaseModel, model_validator


class Viseme(BaseModel):
    offset: int # in milliseconds
    viseme: int # viseme id as in https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-speech-synthesis-viseme?tabs=visemeid&pivots=programming-language-python#map-phonemes-to-visemes

class AudioInstance(BaseModel):
    streaming: bool = False
    content: bytes | AsyncGenerator[bytes, None]
    visemes: Optional[List[Viseme]]

    @model_validator(pre=True)
    def check_content(cls, values):
        streaming, content = values.get('streaming'), values.get('content')
        if streaming and not isinstance(content, AsyncGenerator[bytes, None]):
            raise ValueError('If streaming is True, content must be of BytesIO type')
        return values