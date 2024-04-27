from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class Record(BaseModel):
    """
    A single cache record in the database
    """
    key: str    # unique key (filename) for the file stored in storage
    avatarId: str   # unique key for the avatar, also the folder in storage
    text: str   # text to be converted to audio/video
    filetypes: List[str] # list of file extensions associated with this record. eg: ["mp4"] or ["mp3", "json"]
    created: datetime
    timesUsed: int = 0
    isPersonalization: bool = False # whether the text is main message or for personalization

    @classmethod
    def from_db(cls, record: Dict) -> "Record":
        # copy record to prevent mutating the original dict
        record = record.copy()
        # parse filetypes from str to list
        record['filetypes'] = record['filetypes'].split(',')
        return cls(**record)