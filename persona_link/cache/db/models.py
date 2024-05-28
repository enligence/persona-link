from tortoise import fields
from tortoise.models import Model


class Record(Model):
    """
    A single cache record in the database
    
    Attributes:
        id (int): Primary key for the record, managed by the database.
        key (str): unique key (also filename) for the file stored in storage.
        avatarId (str): unique key for the avatar, also the folder in storage
        text (str): text to be converted to audio/video
        storage_paths (dict): paths where the media and related files are stored
        created (datetime): timestamp when the record was created
        updated (datetime): timestamp of the last update of the record
        metadata (dict): metadata about the record
    """
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=255, unique=True)   # unique key (also filename) for the file stored in storage.
    avatarId = fields.CharField(max_length=255)   # unique key for the avatar, also the folder in storage
    text = fields.TextField()   # text to be converted to audio/video
    storage_paths = fields.JSONField()   # paths where the media and related files are stored
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True, null=True)
    metadata = fields.JSONField(null=True)  # metadata about the record
    
    class Meta:
        table = "records"
        app = "persona_link"
    
class UsageLog(Model):
    """
    A log of usage of a cache record
    
    Attributes:
        id (int): Primary key for the log, managed by the database.
        record (Record): the record for which the usage is logged
        timestamp (datetime): timestamp of the usage
    """
    record = fields.ForeignKeyField('persona_link.Record', related_name='usage_logs', on_delete='CASCADE')
    timestamp = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        app = "persona_link"
        table = "usage_logs"