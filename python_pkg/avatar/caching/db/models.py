from tortoise.models import Model
from tortoise import fields

class DBRecord(Model):
    """
    A single cache record in the database
    """
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=64)
    avatarId = fields.CharField(max_length=64)
    text = fields.TextField()
    filetypes = fields.CharField(max_length=32)
    created = fields.DatetimeField()
    timesUsed = fields.IntField()
    isPersonalization = fields.BooleanField()

    class Meta:
        table = "cache"