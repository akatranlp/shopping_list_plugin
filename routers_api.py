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
    return {"success": True}


@router.get('/units', response_model=List[schemas.ShoppingListPluginUnitOut])
async def get_all() -> List[schemas.ShoppingListPluginUnitOut]:
    return await repo.get_all_units()


@router.post('/units', response_model=schemas.ShoppingListPluginUnitOut)
async def create_unit(unit: schemas.ShoppingListPluginUnitIn,
                      user: schemas_user.User =
                      Depends(oauth2.get_current_active_user)) -> schemas.ShoppingListPluginUnitOut:
    oauth2.check_permission(user)
    return await repo.create_unit(unit)


@router.get('/units/{unit_id}', response_model=schemas.ShoppingListPluginUnitOut)
async def get_unit(unit_id: int) -> schemas.ShoppingListPluginUnitOut:
    return await repo.get_unit(unit_id)


@router.get('/products', response_model=List[schemas.ShoppingListPluginProductOut])
async def my_products(user: models_user.User =
                      Depends(oauth2.get_current_active_user_model)) -> List[schemas.ShoppingListPluginProductOut]:
    return await repo.get_all_products(user)


@router.post('/products', response_model=schemas.ShoppingListPluginProductOut)
async def create_product(product: schemas.ShoppingListPluginProductIn,
                         user: models_user.User =
                         Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPluginProductOut:
    return await repo.create_product(product, user)


@router.get('/products/{uuid}', response_model=schemas.ShoppingListPluginProductOut)
async def get_product(uuid: UUID,
                      user: models_user.User =
                      Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPluginProductOut:
    return await repo.get_product(uuid, user)


@router.put('/products/{uuid}', response_model=schemas.ShoppingListPluginProductOut)
async def change_product(uuid: UUID,
                         product: schemas.ShoppingListPluginProductPut,
                         user: models_user.User =
                         Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPluginProductOut:
    return await repo.change_product(uuid, product, user)


@router.delete('/products/{uuid}', response_model=schemas.ShoppingListPluginProductOut)
async def delete_product(uuid: UUID,
                         user: models_user.User =
                         Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPluginProductOut:
    return await repo.delete_product(uuid, user)


@router.get('/shoppingLists', response_model=List[schemas.ShoppingListPluginList])
async def get_all_shopping_lists(user: models_user.User =
                                 Depends(oauth2.get_current_active_user_model)) -> List[schemas.ShoppingListPluginList]:
    return await repo.get_all_shopping_lists(user)


@router.post('/shoppingLists', response_model=schemas.ShoppingListPluginList)
async def create_shopping_list(s_list: schemas.ShoppingListPluginListIn,
                               user: models_user.User =
                               Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPluginList:
    return await repo.create_shopping_list(s_list, user)


@router.get('/shoppingLists/{uuid}', response_model=schemas.ShoppingListPluginListOut)
async def get_shopping_list(uuid: UUID,
                            user: models_user.User =
                            Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPluginListOut:
    return await repo.get_shopping_list(uuid, user)


@router.post('/shoppingLists/{uuid}', response_model=schemas.ShoppingListPluginListOut)
async def change_shopping_list(uuid: UUID,
                               s_list: schemas.ShoppingListPluginListPut,
                               user: models_user.User =
                               Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPluginListOut:
    return await repo.change_shopping_list(uuid, s_list, user)


@router.delete('/shoppingLists/{uuid}', response_model=schemas.ShoppingListPluginListOut)
async def delete_shopping_list(uuid: UUID,
                               user: models_user.User =
                               Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPluginListOut:
    return await repo.delete_shopping_list(uuid, user)


@router.get('/shoppingLists/{s_list_uuid}/entries', response_model=List[schemas.ShoppingListPluginListEntryOut])
async def get_s_list_entries(s_list_uuid: UUID,
                             user: models_user.User =
                             Depends(
                                 oauth2.get_current_active_user_model)) -> List[schemas.ShoppingListPluginListEntryOut]:
    return await repo.get_s_list_entries(s_list_uuid, user)


@router.post('/shoppingLists/{s_list_uuid}/entries', response_model=schemas.ShoppingListPluginListEntryOut)
async def create_s_list_entry(s_list_uuid: UUID,
                              s_list_entry: schemas.ShoppingListPluginListEntryIn,
                              user: models_user.User =
                              Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPluginListEntryOut:
    return await repo.create_s_list_entry(s_list_uuid, s_list_entry, user)
