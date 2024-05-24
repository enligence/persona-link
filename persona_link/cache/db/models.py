from tortoise.models import Model
from tortoise import fields
class Record(Model):
    """
    A single cache record in the database
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
    record = fields.ForeignKeyField('persona_link.Record', related_name='usage_logs', on_delete='CASCADE')
    timestamp = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        app = "persona_link"
        table = "usage_logs"