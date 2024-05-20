from typing import AsyncGenerator, List, Optional
from pydantic import BaseModel, model_validator, ConfigDict


class Viseme(BaseModel):
    offset: int # in milliseconds
    viseme: int # viseme id as in https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-speech-synthesis-viseme?tabs=visemeid&pivots=programming-language-python#map-phonemes-to-visemes

class WordTimestamp(BaseModel):
    word: str # word spoken
    offset: int # in milliseconds
    duration: int # in milliseconds
    text_offset: int # offset in text
    word_length: int # length of the word spoken
class AudioInstance(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed = True)  #skip the validation for any custom/unrecognized types. like AsyncGenerator
    
    streaming: bool = False
    content: bytes | AsyncGenerator[bytes, None]
    visemes: Optional[List[Viseme]]
    word_timestamps: Optional[List[WordTimestamp]]

    @model_validator(mode = 'after')
    def check_content(cls, values):
        streaming, content = values.get('streaming'), values.get('content')
        if streaming and not isinstance(content, AsyncGenerator[bytes, None]):
            raise ValueError('If streaming is True, content must be of BytesIO type')
        return values