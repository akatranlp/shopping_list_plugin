from typing import List
from fastapi import HTTPException, status
from . import models, schemas
from ...models import models_user


async def get_all_units() -> List[schemas.ShoppingListPluginUnit]:
    unit_list = []
    async for unit in models.ShoppingListPluginUnit.all():
        unit_list.append(await schemas.ShoppingListPluginUnit.from_tortoise_orm(unit))
    return unit_list


async def create_unit(unit: schemas.ShoppingListPluginUnitIn) -> schemas.ShoppingListPluginUnit:
    unit_obj = models.ShoppingListPluginUnit(unit=unit.unit)
    try:
        await unit_obj.save()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Hat nicht funktioniert')
    return await schemas.ShoppingListPluginUnit.from_tortoise_orm(unit_obj)


async def get_unit(unit_id: int) -> schemas.ShoppingListPluginUnit:
    unit_obj = await models.ShoppingListPluginUnit.get(id=unit_id)
    if not unit_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Unit does not exist')
    return await schemas.ShoppingListPluginUnit.from_tortoise_orm(unit_obj)


async def get_all_products(user: models_user.User):
    product_list = []
    async for product_obj in models.ShoppingListPluginProduct.filter(creator=user):
        product_list.append(await schemas.ShoppingListPluginProduct.from_tortoise_orm(product_obj))
    return product_list


async def create_product(product: schemas.ShoppingListPluginProductIn, user: models_user.User):
    unit_obj = await models.ShoppingListPluginUnit.get(id=product.unit_id)
    if not unit_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Unit does not exist')

    product_obj = models.ShoppingListPluginProduct(
        name=product.name,
        unit_type=unit_obj,
        creator=user
    )
    try:
        await product_obj.save()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Hat nicht funktioniert')
    return await schemas.ShoppingListPluginProduct.from_tortoise_orm(product_obj)
