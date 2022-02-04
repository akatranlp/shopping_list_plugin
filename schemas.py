import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Extra
from tortoise.contrib.pydantic import pydantic_model_creator
from . import models

ShoppingListPlugin_Unit = pydantic_model_creator(models.ShoppingListPlugin_Unit, name="ShoppingListPlugin_Unit")
ShoppingListPlugin_UnitIn = pydantic_model_creator(models.ShoppingListPlugin_Unit, name="ShoppingListPlugin_UnitIn",
                                                   exclude_readonly=True)
ShoppingListPlugin_UnitOut = pydantic_model_creator(models.ShoppingListPlugin_Unit, name="ShoppingListPlugin_UnitOut")

ShoppingListPlugin_Product = pydantic_model_creator(models.ShoppingListPlugin_Product,
                                                    name="ShoppingListPlugin_Product")


class ShoppingListPlugin_ProductIn(BaseModel):
    name: str
    pic_url: Optional[str]
    unit_id: int

    class Config:
        extra = Extra.forbid


class ShoppingListPlugin_ProductPut(BaseModel):
    name: Optional[str]
    pic_url: Optional[str]
    unit_id: Optional[int]

    class Config:
        extra = Extra.forbid


class ShoppingListPlugin_ProductOut(BaseModel):
    uuid: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str
    pic_url: Optional[str]
    unit_type: str

    class Config:
        extra = Extra.forbid

    @classmethod
    async def from_model(cls, model: models.ShoppingListPlugin_Product):
        return ShoppingListPlugin_ProductOut(
            uuid=model.uuid,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            pic_url=model.pic_url,
            unit_type=(await model.unit_type).unit,

        )


ShoppingListPlugin_ListEntry = pydantic_model_creator(models.ShoppingListPlugin_ListEntry,
                                                      name="ShoppingListPlugin_ListEntry")


class ShoppingListPlugin_ListEntryIn(BaseModel):
    product_uuid: UUID
    amount: float

    class Config:
        extra = Extra.forbid


class ShoppingListPlugin_ListEntryOut(BaseModel):
    uuid: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    product_uuid: UUID
    product_name: str
    product_pic_url: Optional[str]
    product_unit_type: str
    amount: float

    class Config:
        extra = Extra.forbid

    @classmethod
    async def from_model(cls, model: models.ShoppingListPlugin_ListEntry):
        product: models.ShoppingListPlugin_Product = await model.product
        return ShoppingListPlugin_ListEntryOut(
            uuid=model.uuid,
            created_at=model.created_at,
            updated_at=model.updated_at,
            product_uuid=product.uuid,
            product_name=product.name,
            product_pic_url=product.pic_url,
            product_unit_type=(await product.unit_type).unit,
            amount=model.amount

        )


class ShoppingListPlugin_ListEntryPut(BaseModel):
    product_uuid: Optional[UUID]
    amount: Optional[float]

    class Config:
        extra = Extra.forbid


ShoppingListPlugin_List = pydantic_model_creator(models.ShoppingListPlugin_List, name="ShoppingListPlugin_List")
ShoppingListPlugin_ListIn = pydantic_model_creator(models.ShoppingListPlugin_List, name="ShoppingListPlugin_ListIn",
                                                   exclude_readonly=True)


class ShoppingListPlugin_ListOut(BaseModel):
    uuid: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str
    entries: List[ShoppingListPlugin_ListEntryOut]

    class Config:
        extra = Extra.forbid

    @classmethod
    async def from_model(cls, model: models.ShoppingListPlugin_List):
        entries = []
        async for entry in models.ShoppingListPlugin_ListEntry.filter(shoppinglist=model):
            entries.append(await ShoppingListPlugin_ListEntryOut.from_model(entry))
        return ShoppingListPlugin_ListOut(
            uuid=model.uuid,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            entries=entries
        )


class ShoppingListPlugin_ListPut(BaseModel):
    name: Optional[str]

    class Config:
        extra = Extra.forbid
