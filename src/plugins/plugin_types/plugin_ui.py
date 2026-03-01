# Python imports

# Lib imports

# Application imports
from libs.dto.base_event import BaseEvent

from ..plugin_context import PluginContext
from .plugin_base import PluginBase



class PluginCodeException(Exception):
    ...



class PluginUI(PluginBase):
    def __init__(self, *args, **kwargs):
        super(PluginUI, self).__init__(*args, **kwargs)

        self.plugin_context: PluginContext = None


    def _controller_message(self, event: BaseEvent):
        raise PluginCodeException("Plugin UI '_controller_message' must be overriden by Plugin")

    def load(self):
        raise PluginCodeException("Plugin UI 'load' must be overriden by Plugin")

    def run(self):
        raise PluginCodeException("Plugin UI 'run' must be overriden by Plugin")

    def request_ui_element(self, element_id: str):
        return self.plugin_context.request_ui_element(element_id)

    def emit(self, event: BaseEvent):
        return self.plugin_context.emit(event)

    def emit_to(self, name: str, event: BaseEvent):
        return self.plugin_context.emit_to(name, event)

    def emit_to_selected(self, names: list[str], event: BaseEvent):
        return self.plugin_context.emit_to_selected(names, event)
