from fastapi.templating import Jinja2Templates
from py_api.routers.routers_helper import APIRouter

PLUGIN_NAME = 'shopping_list_plugin'

templates = Jinja2Templates(directory=f"py_api/plugins/{PLUGIN_NAME}/templates")
router = APIRouter(
    prefix=f'/plugin/{PLUGIN_NAME}/api',
    tags=[PLUGIN_NAME],
)


@router.get('/')
def get_index():
    return {"success": True}
