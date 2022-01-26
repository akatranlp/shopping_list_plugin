import datetime
from typing import Optional, List
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
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str
    unit_type: str

    class Config:
        extra = Extra.forbid

    @classmethod
    async def from_model(cls, model: models.ShoppingListPluginProduct):
        return ShoppingListPluginProductOut(
            uuid=model.uuid,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            unit_type=(await model.unit_type).unit,

        )


ShoppingListPluginListEntry = pydantic_model_creator(models.ShoppingListPluginListEntry,
                                                     name="ShoppingListPluginListEntry")


class ShoppingListPluginListEntryIn(BaseModel):
    product_uuid: UUID
    amount: float

    class Config:
        extra = Extra.forbid


class ShoppingListPluginListEntryOut(BaseModel):
    uuid: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    product_uuid: UUID
    product_name: str
    product_unit_type: str
    amount: float

    class Config:
        extra = Extra.forbid

    @classmethod
    async def from_model(cls, model: models.ShoppingListPluginListEntry):
        product: models.ShoppingListPluginProduct = await model.product
        return ShoppingListPluginListEntryOut(
            uuid=model.uuid,
            created_at=model.created_at,
            updated_at=model.updated_at,
            product_uuid=product.uuid,
            product_name=product.name,
            product_unit_type=(await product.unit_type).unit,
            amount=model.amount

        )


class ShoppingListPluginListEntryPut(BaseModel):
    product_uuid: Optional[UUID]
    amount: Optional[float]

    class Config:
        extra = Extra.forbid


ShoppingListPluginList = pydantic_model_creator(models.ShoppingListPluginList, name="ShoppingListPluginList")
ShoppingListPluginListIn = pydantic_model_creator(models.ShoppingListPluginList, name="ShoppingListPluginListIn",
                                                  exclude_readonly=True)


class ShoppingListPluginListOut(BaseModel):
    uuid: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str
    entries: List[ShoppingListPluginListEntryOut]

    class Config:
        extra = Extra.forbid

    @classmethod
    async def from_model(cls, model: models.ShoppingListPluginList):
        entries = []
        async for entry in models.ShoppingListPluginListEntry.filter(shoppinglist=model):
            entries.append(await ShoppingListPluginListEntryOut.from_model(entry))
        return ShoppingListPluginListOut(
            uuid=model.uuid,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            entries=entries
        )


class ShoppingListPluginListPut(BaseModel):
    name: Optional[str]

    class Config:
        extra = Extra.forbid
