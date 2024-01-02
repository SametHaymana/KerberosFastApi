from tortoise import fields
from tortoise.models import Model

class Servers(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, required=True)
    secret = fields.CharField(max_length=255, required=True)

    class Meta:
        table = "servers"

    def __str__(self):
        return self.name
