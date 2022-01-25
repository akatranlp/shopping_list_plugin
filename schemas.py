from tortoise.contrib.pydantic import pydantic_model_creator
from . import models

ShoppingListPluginUnit = pydantic_model_creator(models.ShoppingListPluginUnit, name="ShoppingListPluginUnit")
ShoppingListPluginUnitIn = pydantic_model_creator(models.ShoppingListPluginUnit, name="ShoppingListPluginUnitIn",
                                                  exclude_readonly=True)
ShoppingListPluginUnitOut = pydantic_model_creator(models.ShoppingListPluginUnit, name="ShoppingListPluginUnitOut")


ShoppingListPluginProduct = pydantic_model_creator(models.ShoppingListPluginProduct, name="ShoppingListPluginProduct")
ShoppingListPluginProductIn = pydantic_model_creator(models.ShoppingListPluginProduct,
                                                     name="ShoppingListPluginProductIn")
ShoppingListPluginProductOut = pydantic_model_creator(models.ShoppingListPluginProduct,
                                                      name="ShoppingListPluginProductOut")
