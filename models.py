from tortoise.models import Model
from tortoise import fields


class ShoppingListPlugin_DBBaseModel:
    uuid = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class ShoppingListPlugin_Unit(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    unit = fields.CharField(10, unique=True)


class ShoppingListPlugin_Product(ShoppingListPlugin_DBBaseModel, Model):
    name = fields.CharField(50)
    pic_url = fields.TextField(default="")
    unit_type = fields.ForeignKeyField("models.ShoppingListPlugin_Unit", related_name="shoppingListPluginProduct")
    creator = fields.ForeignKeyField("models.User", related_name="shoppingListPluginProduct")


class ShoppingListPlugin_List(ShoppingListPlugin_DBBaseModel, Model):
    name = fields.CharField(128)
    creator = fields.ForeignKeyField("models.User", related_name="shoppingListPluginList")


class ShoppingListPlugin_ListEntry(ShoppingListPlugin_DBBaseModel, Model):
    shoppinglist = fields.ForeignKeyField("models.ShoppingListPlugin_List", related_name="shoppingListPluginListEntry")
    product = fields.ForeignKeyField("models.ShoppingListPlugin_Product", related_name="shoppingListPluginListEntry")
    amount = fields.FloatField()
