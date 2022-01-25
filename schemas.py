from pydantic import BaseModel, Extra
from tortoise.contrib.pydantic import pydantic_model_creator
from . import models

ShoppingListPluginUnit = pydantic_model_creator(models.ShoppingListPluginUnit, name="ShoppingListPluginUnit")
ShoppingListPluginUnitIn = pydantic_model_creator(models.ShoppingListPluginUnit, name="ShoppingListPluginUnitIn",
                                                  exclude_readonly=True)
ShoppingListPluginUnitOut = pydantic_model_creator(models.ShoppingListPluginUnit, name="ShoppingListPluginUnitOut")

ShoppingListPluginProduct = pydantic_model_creator(models.ShoppingListPluginProduct, name="ShoppingListPluginProduct")


class ShoppingListPluginProductIn(BaseModel):
    name: str
    unit_id: int

    class Config:
        extra = Extra.forbid


ShoppingListPluginProductOut = pydantic_model_creator(models.ShoppingListPluginProduct,
                                                      name="ShoppingListPluginProductOut")
