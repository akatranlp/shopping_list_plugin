from tortoise.models import Model
from tortoise import fields


class ShoppingListPluginDBBaseModel:
    uuid = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class ShoppingListPluginUnit(ShoppingListPluginDBBaseModel, Model):
    unit = fields.CharField(10, unique=True)


class ShoppingListPluginProduct(ShoppingListPluginDBBaseModel, Model):
    name = fields.CharField(50, unique=True)
    unit_type = fields.ForeignKeyField("models.ShoppingListPluginUnit", related_name="shoppingListPluginProduct")
    creator = fields.ForeignKeyField("models.User", related_name="shoppingListPluginProduct")


class ShoppingListPluginList(ShoppingListPluginDBBaseModel, Model):
    creator = fields.ForeignKeyField("models.User", related_name="shoppingListPluginList")


class ShoppingListPluginListEntry(Model):
    shoppinglist = fields.ForeignKeyField("models.ShoppingListPluginList", related_name="shoppingListPluginListEntry")
    product = fields.ForeignKeyField("models.ShoppingListPluginProduct", related_name="shoppingListPluginListEntry")
    amount = fields.FloatField()
