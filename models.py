from tortoise.models import Model
from tortoise import fields


class ExamplePluginTestModel(Model):
    id = fields.IntField(pk=True)
