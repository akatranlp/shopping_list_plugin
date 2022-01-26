from typing import List
from uuid import UUID

from fastapi import Depends
from fastapi.templating import Jinja2Templates
from py_api.routers.routers_helper import APIRouter
from . import schemas, repo
from ... import oauth2
from ...models import models_user
from ...schemas import schemas_user

PLUGIN_NAME = 'shopping_list_plugin'

templates = Jinja2Templates(directory=f"py_api/plugins/{PLUGIN_NAME}/templates")
router = APIRouter(
    prefix=f'/plugin/{PLUGIN_NAME}/api',
    tags=[PLUGIN_NAME],
)


@router.get('/')
def get_index():
    return {"success": True, "message": "ShoppingListPlugin loaded"}


@router.get('/units', response_model=List[schemas.ShoppingListPlugin_UnitOut])
async def get_all() -> List[schemas.ShoppingListPlugin_UnitOut]:
    return await repo.get_all_units()


@router.post('/units', response_model=schemas.ShoppingListPlugin_UnitOut)
async def create_unit(unit: schemas.ShoppingListPlugin_UnitIn,
                      user: schemas_user.User =
                      Depends(oauth2.get_current_active_user)) -> schemas.ShoppingListPlugin_UnitOut:
    oauth2.check_permission(user)
    return await repo.create_unit(unit)


@router.get('/units/{unit_id}', response_model=schemas.ShoppingListPlugin_UnitOut)
async def get_unit(unit_id: int) -> schemas.ShoppingListPlugin_UnitOut:
    return await repo.get_unit(unit_id)


@router.get('/products', response_model=List[schemas.ShoppingListPlugin_ProductOut])
async def my_products(user: models_user.User =
                      Depends(oauth2.get_current_active_user_model)) -> List[schemas.ShoppingListPlugin_ProductOut]:
    return await repo.get_all_products(user)


@router.post('/products', response_model=schemas.ShoppingListPlugin_ProductOut)
async def create_product(product: schemas.ShoppingListPlugin_ProductIn,
                         user: models_user.User =
                         Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPlugin_ProductOut:
    return await repo.create_product(product, user)


@router.get('/products/{uuid}', response_model=schemas.ShoppingListPlugin_ProductOut)
async def get_product(uuid: UUID,
                      user: models_user.User =
                      Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPlugin_ProductOut:
    return await repo.get_product(uuid, user)


@router.put('/products/{uuid}', response_model=schemas.ShoppingListPlugin_ProductOut)
async def change_product(uuid: UUID,
                         product: schemas.ShoppingListPlugin_ProductPut,
                         user: models_user.User =
                         Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPlugin_ProductOut:
    return await repo.change_product(uuid, product, user)


@router.delete('/products/{uuid}', response_model=schemas.ShoppingListPlugin_ProductOut)
async def delete_product(uuid: UUID,
                         user: models_user.User =
                         Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPlugin_ProductOut:
    return await repo.delete_product(uuid, user)


@router.get('/shoppingLists', response_model=List[schemas.ShoppingListPlugin_List])
async def get_all_shopping_lists(user: models_user.User =
                                 Depends(oauth2.get_current_active_user_model)) -> List[
    schemas.ShoppingListPlugin_List]:
    return await repo.get_all_shopping_lists(user)


@router.post('/shoppingLists', response_model=schemas.ShoppingListPlugin_List)
async def create_shopping_list(s_list: schemas.ShoppingListPlugin_ListIn,
                               user: models_user.User =
                               Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPlugin_List:
    return await repo.create_shopping_list(s_list, user)


@router.get('/shoppingLists/{uuid}', response_model=schemas.ShoppingListPlugin_ListOut)
async def get_shopping_list(uuid: UUID,
                            user: models_user.User =
                            Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPlugin_ListOut:
    return await repo.get_shopping_list(uuid, user)


@router.put('/shoppingLists/{uuid}', response_model=schemas.ShoppingListPlugin_ListOut)
async def change_shopping_list(uuid: UUID,
                               s_list: schemas.ShoppingListPlugin_ListPut,
                               user: models_user.User =
                               Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPlugin_ListOut:
    return await repo.change_shopping_list(uuid, s_list, user)


@router.delete('/shoppingLists/{uuid}', response_model=schemas.ShoppingListPlugin_ListOut)
async def delete_shopping_list(uuid: UUID,
                               user: models_user.User =
                               Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPlugin_ListOut:
    return await repo.delete_shopping_list(uuid, user)


@router.get('/shoppingLists/{s_list_uuid}/entries', response_model=List[schemas.ShoppingListPlugin_ListEntryOut],
            name="Get All Shopping List Entries")
async def get_s_list_entries(s_list_uuid: UUID,
                             user: models_user.User =
                             Depends(
                                 oauth2.get_current_active_user_model)) -> List[
    schemas.ShoppingListPlugin_ListEntryOut]:
    return await repo.get_s_list_entries(s_list_uuid, user)


@router.post('/shoppingLists/{s_list_uuid}/entries', response_model=schemas.ShoppingListPlugin_ListEntryOut,
             name="Create Shopping List Entry")
async def create_s_list_entry(s_list_uuid: UUID,
                              s_list_entry: schemas.ShoppingListPlugin_ListEntryIn,
                              user: models_user.User =
                              Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPlugin_ListEntryOut:
    return await repo.create_s_list_entry(s_list_uuid, s_list_entry, user)


@router.get('/shoppingLists/{s_list_uuid}/entries/{uuid}', response_model=schemas.ShoppingListPlugin_ListEntryOut,
            name="Get Shopping List Entry")
async def get_s_list_entry(s_list_uuid: UUID,
                           uuid: UUID,
                           user: models_user.User =
                           Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPlugin_ListEntryOut:
    return await repo.get_s_list_entry(s_list_uuid, uuid, user)


@router.put('/shoppingLists/{s_list_uuid}/entries/{uuid}', response_model=schemas.ShoppingListPlugin_ListEntryOut,
            name="Change Shopping List Entry")
async def change_s_list_entry(s_list_uuid: UUID,
                              uuid: UUID,
                              s_list_entry: schemas.ShoppingListPlugin_ListEntryPut,
                              user: models_user.User =
                              Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPlugin_ListEntryOut:
    return await repo.change_s_list_entry(s_list_uuid, uuid, s_list_entry, user)


@router.delete('/shoppingLists/{s_list_uuid}/entries/{uuid}', response_model=schemas.ShoppingListPlugin_ListEntryOut,
               name="Delete Shopping List Entry")
async def delete_s_list_entry(s_list_uuid: UUID,
                              uuid: UUID,
                              user: models_user.User =
                              Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPlugin_ListEntryOut:
    return await repo.delete_s_list_entry(s_list_uuid, uuid, user)
