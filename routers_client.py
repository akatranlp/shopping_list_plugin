from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

PLUGIN_NAME = 'shopping_list_plugin'

templates = Jinja2Templates(directory=f"py_api/plugins/{PLUGIN_NAME}/templates")

router = APIRouter(
    prefix=f'/plugin/{PLUGIN_NAME}',
    tags=[PLUGIN_NAME],
)


@router.get('/', response_class=HTMLResponse, include_in_schema=False)
async def get_index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/unit', response_class=HTMLResponse, include_in_schema=False)
async def get_unit(request: Request):
    return templates.TemplateResponse('unit_not_final.html', {'request': request})
