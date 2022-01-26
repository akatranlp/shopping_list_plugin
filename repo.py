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


async def get_all_products(user: models_user.User) -> List[schemas.ShoppingListPluginProductOut]:
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product does not exist')
    return product_obj


async def get_product(uuid: UUID, user: models_user.User) -> schemas.ShoppingListPluginProductOut:
    return await schemas.ShoppingListPluginProductOut.from_model(await _get_product(uuid, user))


async def change_product(uuid: UUID,
                         product: schemas.ShoppingListPluginProductPut,
                         user: models_user.User) -> schemas.ShoppingListPluginProductOut:
    product_obj = await _get_product(uuid, user)
    if product.unit_id:
        product_obj.unit_type = await _get_unit(product.unit_id)
    if product.name:
        product_obj.name = product.name

    await product_obj.save()
    return await schemas.ShoppingListPluginProductOut.from_model(product_obj)


async def delete_product(uuid: UUID, user: models_user.User) -> schemas.ShoppingListPluginProductOut:
    product_obj = await _get_product(uuid, user)
    product = await schemas.ShoppingListPluginProductOut.from_model(product_obj)
    await product_obj.delete()
    return product


async def get_all_shopping_lists(user: models_user.User) -> List[schemas.ShoppingListPluginList]:
    shopping_lists = []
    async for s_list in models.ShoppingListPluginList.filter(creator=user):
        shopping_lists.append(await schemas.ShoppingListPluginList.from_tortoise_orm(s_list))
    return shopping_lists


async def create_shopping_list(s_list: schemas.ShoppingListPluginListIn,
                               user: models_user.User) -> schemas.ShoppingListPluginList:
    s_list_obj = models.ShoppingListPluginList(
        name=s_list.name,
        creator=user
    )
    try:
        await s_list_obj.save()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Hat nicht funktioniert')
    return await schemas.ShoppingListPluginList.from_tortoise_orm(s_list_obj)


async def _get_shopping_list(uuid: UUID, user: models_user) -> models.ShoppingListPluginList:
    s_list_obj = await models.ShoppingListPluginList.get(uuid=uuid, creator=user)
    if not s_list_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='List does not exist')
    return s_list_obj


async def get_shopping_list(uuid: UUID, user: models_user) -> schemas.ShoppingListPluginListOut:
    return await schemas.ShoppingListPluginListOut.from_model(await _get_shopping_list(uuid, user))


async def change_shopping_list(uuid: UUID, s_list: schemas.ShoppingListPluginListPut,
                               user: models_user.User) -> schemas.ShoppingListPluginListOut:
    s_list_obj = await _get_shopping_list(uuid, user)
    if s_list.name:
        s_list_obj.name = s_list.name
    await s_list_obj.save()
    return await schemas.ShoppingListPluginListOut.from_model(s_list_obj)


async def delete_shopping_list(uuid: UUID, user: models_user.User) -> schemas.ShoppingListPluginListOut:
    s_list_obj = await _get_shopping_list(uuid, user)
    s_list = await schemas.ShoppingListPluginListOut.from_model(s_list_obj)
    await s_list_obj.delete()
    return s_list


async def get_s_list_entries(s_list_uuid: UUID,
                             user: models_user.User) -> List[schemas.ShoppingListPluginListEntryOut]:
    return (await get_shopping_list(s_list_uuid, user)).entries


async def create_s_list_entry(s_list_uuid: UUID,
                              s_list_entry: schemas.ShoppingListPluginListEntryIn,
                              user: models_user.User) -> schemas.ShoppingListPluginListEntryOut:
    s_list_obj = await _get_shopping_list(s_list_uuid, user)
    product_obj = await _get_product(s_list_entry.product_uuid, user)
    s_list_entry_obj = models.ShoppingListPluginListEntry(
        shoppinglist=s_list_obj,
        product=product_obj,
        amount=s_list_entry.amount
    )
    try:
        await s_list_entry_obj.save()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Hat nicht funktioniert')
    return await schemas.ShoppingListPluginListEntryOut.from_model(s_list_entry_obj)


async def _get_s_list_entry(s_list_uuid: UUID,
                            uuid: UUID,
                            user: models_user.User) -> models.ShoppingListPluginListEntry:
    s_list_obj = await _get_shopping_list(s_list_uuid, user)
    s_list_entry_obj = await models.ShoppingListPluginListEntry.get(uuid=uuid, shoppinglist=s_list_obj)
    if not s_list_entry_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='List Entry does not exist')
    return s_list_entry_obj


async def get_s_list_entry(s_list_uuid: UUID,
                           uuid: UUID,
                           user: models_user.User) -> schemas.ShoppingListPluginListEntryOut:
    return await schemas.ShoppingListPluginListEntryOut.from_model(await _get_s_list_entry(s_list_uuid, uuid, user))


async def change_s_list_entry(s_list_uuid: UUID,
                              uuid: UUID,
                              s_list_entry: schemas.ShoppingListPluginListEntryPut,
                              user: models_user.User) -> schemas.ShoppingListPluginListEntryOut:
    s_list_entry_obj = await _get_s_list_entry(s_list_uuid, uuid, user)
    if s_list_entry.product_uuid:
        s_list_entry_obj.product = await _get_product(s_list_entry.product_uuid, user)
    if s_list_entry.amount:
        s_list_entry_obj.amount = s_list_entry.amount
    await s_list_entry_obj.save()
    return await schemas.ShoppingListPluginListEntryOut.from_model(s_list_entry_obj)
