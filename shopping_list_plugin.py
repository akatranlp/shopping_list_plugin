from typing import List
from py_api.plugins.plugin_helper import PluginInterface
from py_api.routers.routers_helper import APIRouter
from . import routers_api, routers_client

PLUGIN_NAME = 'shopping_list_plugin'


class Plugin(PluginInterface):
    def __init__(self):
        self.name = PLUGIN_NAME
        self.routers = []
        self.has_static_files = True
        self.models = [f'py_api.plugins.{PLUGIN_NAME}.models']
        self.needed_env_keys = []

    def serve_routers(self) -> List[APIRouter]:
        return [routers_api.router, routers_client.router]

