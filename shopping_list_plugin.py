from typing import List

from py_api.plugins.plugin_helper import PluginInterface
from py_api.routers.routers_helper import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

PLUGIN_NAME = 'shopping_list_plugin'


class Plugin(PluginInterface):
    def __init__(self):
        self.name = PLUGIN_NAME
        self.routers = []
        self.has_static_files = True
        self.models = [f'py_api.plugins.{PLUGIN_NAME}.models']
        self.needed_env_keys = []

    def serve_routers(self) -> List[APIRouter]:
        templates = Jinja2Templates(directory=f"py_api/plugins/{PLUGIN_NAME}/templates")
        router = APIRouter(
            prefix=f'/plugin/{PLUGIN_NAME}',
            tags=[PLUGIN_NAME],
        )

        @router.get('/hello_world')
        def get_index():
            return {"success": True}

        @router.get('/', response_class=HTMLResponse, include_in_schema=False)
        async def get_index(request: Request):
            return templates.TemplateResponse('index.html', {'request': request})

        return [router]
