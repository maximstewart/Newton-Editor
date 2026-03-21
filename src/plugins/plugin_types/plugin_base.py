# Python imports

# Lib imports

# Application imports
from libs.dto.base_event import BaseEvent

from ..plugin_context import PluginContext



class PluginBaseException(Exception):
    ...



class PluginBase:
    def __init__(self, *args, **kwargs):
        super(PluginBase, self).__init__(*args, **kwargs)

        self.plugin_context: PluginContext = None


    def _controller_message(self, event: BaseEvent):
        raise PluginBaseException("Plugin Base '_controller_message' must be overriden by Plugin")

    def load(self):
        raise PluginBaseException("Plugin Base 'load' must be overriden by Plugin")

    def unload(self):
        raise PluginBaseException("Plugin Base 'unload' must be overriden by Plugin")

    def run(self):
        raise PluginBaseException("Plugin Base 'run' must be overriden by Plugin")

    def request_ui_element(self, element_id: str):
        raise PluginBaseException("Plugin Base 'request_ui_element' must be overriden by Plugin")

    def emit(self, event: BaseEvent):
        raise PluginBaseException("Plugin Base 'emit' must be overriden by Plugin")

    def emit_to(self, name: str, event: BaseEvent):
        raise PluginBaseException("Plugin Base 'emit_to' must be overriden by Plugin")

    def emit_to_selected(self, names: list[str], event: BaseEvent):
        raise PluginBaseException("Plugin Base 'emit_to_selected' must be overriden by Plugin")
