from typing import List

from fastapi import Depends
from fastapi.templating import Jinja2Templates
from py_api.routers.routers_helper import APIRouter
from . import schemas, repo
from ... import oauth2
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


@router.get('/units', response_model=List[schemas.ShoppingListPluginUnit])
async def get_all() -> List[schemas.ShoppingListPluginUnit]:
    return await repo.get_all()


@router.post('/units', response_model=schemas.ShoppingListPluginUnit)
async def create_unit(unit: schemas.ShoppingListPluginUnitIn,
                      user: schemas_user.User =
                      Depends(oauth2.get_current_active_user_model)) -> schemas.ShoppingListPluginUnit:
    oauth2.check_permission(user)
    return await repo.create_unit(unit)
