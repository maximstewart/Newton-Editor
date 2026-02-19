# Python imports

# Lib imports

# Application imports
from libs.dto.base_event import BaseEvent

from ..plugin_context import PluginContext
from .plugin_base import PluginBase



class PluginCodeException(Exception):
    ...



class PluginCode(PluginBase):
    def __init__(self, *args, **kwargs):
        super(PluginCode, self).__init__(*args, **kwargs)

        self.plugin_context: PluginContext = None


    def _controller_message(self, event: BaseEvent):
        raise PluginCodeException("Plugin Code '_controller_message' must be overriden by Plugin")

    def load(self):
        raise PluginCodeException("Plugin Code 'load' must be overriden by Plugin")

    def run(self):
        raise PluginCodeException("Plugin Code 'run' must be overriden by Plugin")

    def requests_ui_element(self, element_id: str):
        return self.plugin_context.requests_ui_element(element_id)

    def message(self, event: BaseEvent):
        return self.plugin_context.message(event)

    def message_to(self, name: str, event: BaseEvent):
        return self.plugin_context.message_to(name, event)

    def message_to_selected(self, names: list[str], event: BaseEvent):
        return self.plugin_context.message_to_selected(names, event)
