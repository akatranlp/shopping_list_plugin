import datetime
from typing import Optional
from uuid import UUID

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


class ShoppingListPluginProductPut(BaseModel):
    name: Optional[str]
    unit_id: Optional[int]

    class Config:
        extra = Extra.forbid


class ShoppingListPluginProductOut(BaseModel):
    uuid: UUID
    name: str
    unit_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        extra = Extra.forbid

    @classmethod
    async def from_model(cls, model: models.ShoppingListPluginProduct):
        return ShoppingListPluginProductOut(
            uuid=model.uuid,
            name=model.name,
            unit_id=(await model.unit_type).id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
