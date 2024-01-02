from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255)  
    isAdministrator = fields.BooleanField(default=False)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username
