from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from . import models, schemas
from ...models import models_user


async def get_all_units() -> List[schemas.ShoppingListPlugin_UnitOut]:
    unit_list = []
    async for unit in models.ShoppingListPlugin_Unit.all():
        unit_list.append(await schemas.ShoppingListPlugin_UnitOut.from_tortoise_orm(unit))
    return unit_list


async def create_unit(unit: schemas.ShoppingListPlugin_UnitIn) -> schemas.ShoppingListPlugin_UnitOut:
    unit_obj = models.ShoppingListPlugin_Unit(unit=unit.unit)
    try:
        await unit_obj.save()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Hat nicht funktioniert')
    return await schemas.ShoppingListPlugin_UnitOut.from_tortoise_orm(unit_obj)


async def _get_unit(unit_id: int) -> models.ShoppingListPlugin_Unit:
    unit_obj = await models.ShoppingListPlugin_Unit.get(id=unit_id)
    if not unit_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Unit does not exist')
    return unit_obj


async def get_unit(unit_id: int) -> schemas.ShoppingListPlugin_UnitOut:
    return await schemas.ShoppingListPlugin_UnitOut.from_tortoise_orm(await _get_unit(unit_id))


async def get_all_products(user: models_user.User) -> List[schemas.ShoppingListPlugin_ProductOut]:
    product_list = []
    async for product_obj in models.ShoppingListPlugin_Product.filter(creator=user):
        product_list.append(await schemas.ShoppingListPlugin_ProductOut.from_model(product_obj))
    return product_list


def check_url(pic_url: Optional[str]):
    if pic_url and not pic_url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.ico', '.webp')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='url does not endwith .jpg or .jpeg or .png or .gif or .ico or .webp')


async def create_product(product: schemas.ShoppingListPlugin_ProductIn, user: models_user.User):
    unit_obj = await models.ShoppingListPlugin_Unit.get(id=product.unit_id)
    if not unit_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Unit does not exist')
    check_url(product.pic_url)
    product_obj = models.ShoppingListPlugin_Product(
        name=product.name,
        pic_url=product.pic_url,
        unit_type=unit_obj,
        creator=user
    )
    try:
        await product_obj.save()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Hat nicht funktioniert')
    return await schemas.ShoppingListPlugin_ProductOut.from_model(product_obj)


async def _get_product(uuid: UUID, user: models_user.User) -> models.ShoppingListPlugin_Product:
    product_obj = await models.ShoppingListPlugin_Product.get(uuid=uuid, creator=user)
    if not product_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product does not exist')
    return product_obj


async def get_product(uuid: UUID, user: models_user.User) -> schemas.ShoppingListPlugin_ProductOut:
    return await schemas.ShoppingListPlugin_ProductOut.from_model(await _get_product(uuid, user))


async def change_product(uuid: UUID,
                         product: schemas.ShoppingListPlugin_ProductPut,
                         user: models_user.User) -> schemas.ShoppingListPlugin_ProductOut:
    product_obj = await _get_product(uuid, user)
    check_url(product.pic_url)
    if product.unit_id:
        product_obj.unit_type = await _get_unit(product.unit_id)
    if product.name:
        product_obj.name = product.name
    if product.pic_url is not None:
        product_obj.pic_url = product.pic_url

    await product_obj.save()
    return await schemas.ShoppingListPlugin_ProductOut.from_model(product_obj)


async def delete_product(uuid: UUID, user: models_user.User) -> schemas.ShoppingListPlugin_ProductOut:
    product_obj = await _get_product(uuid, user)
    product = await schemas.ShoppingListPlugin_ProductOut.from_model(product_obj)
    await product_obj.delete()
    return product


async def get_all_shopping_lists(user: models_user.User) -> List[schemas.ShoppingListPlugin_List]:
    shopping_lists = []
    async for s_list in models.ShoppingListPlugin_List.filter(creator=user):
        shopping_lists.append(await schemas.ShoppingListPlugin_List.from_tortoise_orm(s_list))
    return shopping_lists


async def create_shopping_list(s_list: schemas.ShoppingListPlugin_ListIn,
                               user: models_user.User) -> schemas.ShoppingListPlugin_List:
    s_list_obj = models.ShoppingListPlugin_List(
        name=s_list.name,
        creator=user
    )
    try:
        await s_list_obj.save()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Hat nicht funktioniert')
    return await schemas.ShoppingListPlugin_List.from_tortoise_orm(s_list_obj)


async def _get_shopping_list(uuid: UUID, user: models_user) -> models.ShoppingListPlugin_List:
    s_list_obj = await models.ShoppingListPlugin_List.get(uuid=uuid, creator=user)
    if not s_list_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='List does not exist')
    return s_list_obj


async def get_shopping_list(uuid: UUID, user: models_user) -> schemas.ShoppingListPlugin_ListOut:
    return await schemas.ShoppingListPlugin_ListOut.from_model(await _get_shopping_list(uuid, user))


async def change_shopping_list(uuid: UUID, s_list: schemas.ShoppingListPlugin_ListPut,
                               user: models_user.User) -> schemas.ShoppingListPlugin_ListOut:
    s_list_obj = await _get_shopping_list(uuid, user)
    if s_list.name:
        s_list_obj.name = s_list.name
    await s_list_obj.save()
    return await schemas.ShoppingListPlugin_ListOut.from_model(s_list_obj)


async def delete_shopping_list(uuid: UUID, user: models_user.User) -> schemas.ShoppingListPlugin_ListOut:
    s_list_obj = await _get_shopping_list(uuid, user)
    s_list = await schemas.ShoppingListPlugin_ListOut.from_model(s_list_obj)
    await s_list_obj.delete()
    return s_list


async def get_s_list_entries(s_list_uuid: UUID,
                             user: models_user.User) -> List[schemas.ShoppingListPlugin_ListEntryOut]:
    return (await get_shopping_list(s_list_uuid, user)).entries


async def create_s_list_entry(s_list_uuid: UUID,
                              s_list_entry: schemas.ShoppingListPlugin_ListEntryIn,
                              user: models_user.User) -> schemas.ShoppingListPlugin_ListEntryOut:
    s_list_obj = await _get_shopping_list(s_list_uuid, user)
    product_obj = await _get_product(s_list_entry.product_uuid, user)
    s_list_entry_obj = models.ShoppingListPlugin_ListEntry(
        shoppinglist=s_list_obj,
        product=product_obj,
        amount=s_list_entry.amount
    )
    try:
        await s_list_entry_obj.save()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Hat nicht funktioniert')
    return await schemas.ShoppingListPlugin_ListEntryOut.from_model(s_list_entry_obj)


async def _get_s_list_entry(s_list_uuid: UUID,
                            uuid: UUID,
                            user: models_user.User) -> models.ShoppingListPlugin_ListEntry:
    s_list_obj = await _get_shopping_list(s_list_uuid, user)
    s_list_entry_obj = await models.ShoppingListPlugin_ListEntry.get(uuid=uuid, shoppinglist=s_list_obj)
    if not s_list_entry_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='List Entry does not exist')
    return s_list_entry_obj


async def get_s_list_entry(s_list_uuid: UUID,
                           uuid: UUID,
                           user: models_user.User) -> schemas.ShoppingListPlugin_ListEntryOut:
    return await schemas.ShoppingListPlugin_ListEntryOut.from_model(await _get_s_list_entry(s_list_uuid, uuid, user))


async def change_s_list_entry(s_list_uuid: UUID,
                              uuid: UUID,
                              s_list_entry: schemas.ShoppingListPlugin_ListEntryPut,
                              user: models_user.User) -> schemas.ShoppingListPlugin_ListEntryOut:
    s_list_entry_obj = await _get_s_list_entry(s_list_uuid, uuid, user)
    if s_list_entry.product_uuid:
        s_list_entry_obj.product = await _get_product(s_list_entry.product_uuid, user)
    if s_list_entry.amount:
        s_list_entry_obj.amount = s_list_entry.amount
    await s_list_entry_obj.save()
    return await schemas.ShoppingListPlugin_ListEntryOut.from_model(s_list_entry_obj)


async def delete_s_list_entry(s_list_uuid: UUID,
                              uuid: UUID,
                              user: models_user.User) -> schemas.ShoppingListPlugin_ListEntryOut:
    s_list_entry_obj = await _get_s_list_entry(s_list_uuid, uuid, user)
    s_list_entry = await schemas.ShoppingListPlugin_ListEntryOut.from_model(s_list_entry_obj)
    await s_list_entry_obj.delete()
    return s_list_entry
