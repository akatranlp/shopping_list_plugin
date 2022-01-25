from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from . import models, schemas
from ...models import models_user


async def get_all_units() -> List[schemas.ShoppingListPluginUnitOut]:
    unit_list = []
    async for unit in models.ShoppingListPluginUnit.all():
        unit_list.append(await schemas.ShoppingListPluginUnitOut.from_tortoise_orm(unit))
    return unit_list


async def create_unit(unit: schemas.ShoppingListPluginUnitIn) -> schemas.ShoppingListPluginUnitOut:
    unit_obj = models.ShoppingListPluginUnit(unit=unit.unit)
    try:
        await unit_obj.save()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Hat nicht funktioniert')
    return await schemas.ShoppingListPluginUnitOut.from_tortoise_orm(unit_obj)


async def _get_unit(unit_id: int) -> models.ShoppingListPluginUnit:
    unit_obj = await models.ShoppingListPluginUnit.get(id=unit_id)
    if not unit_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Unit does not exist')
    return unit_obj


async def get_unit(unit_id: int) -> schemas.ShoppingListPluginUnitOut:
    return await schemas.ShoppingListPluginUnitOut.from_tortoise_orm(await _get_unit(unit_id))


async def get_all_products(user: models_user.User):
    product_list = []
    async for product_obj in models.ShoppingListPluginProduct.filter(creator=user):
        product_list.append(await schemas.ShoppingListPluginProductOut.from_model(product_obj))
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
    return await schemas.ShoppingListPluginProductOut.from_model(product_obj)


async def _get_product(uuid: UUID, user: models_user.User) -> models.ShoppingListPluginProduct:
    product_obj = await models.ShoppingListPluginProduct.get(uuid=uuid, creator=user)
    if not product_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Unit does not exist')
    return product_obj


async def get_product(uuid: UUID, user: models_user.User) -> schemas.ShoppingListPluginProductOut:
    return await schemas.ShoppingListPluginProductOut.from_model(await _get_product(uuid, user))


async def change_product(uuid: UUID,
                         product: schemas.ShoppingListPluginProductPut,
                         user: models_user.User) -> schemas.ShoppingListPluginProductOut:
    product_obj = await _get_product(uuid, user)
    if product.unit_id:
        unit_obj = await _get_unit(product.unit_id)
        product_obj.unit_type = unit_obj
    if product.name:
        product_obj.name = product.name

    await product_obj.save()
    return await schemas.ShoppingListPluginProductOut.from_model(product_obj)


async def delete_product(uuid: UUID, user: models_user.User) -> schemas.ShoppingListPluginProductOut:
    product_obj = await _get_product(uuid, user)
    product = await schemas.ShoppingListPluginProductOut.from_model(product_obj)
    await product_obj.delete()
    return product
