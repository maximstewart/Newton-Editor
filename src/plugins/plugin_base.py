# Python imports

# Lib imports

# Application imports
from libs.dto.base_event import BaseEvent

from .plugin_context import PluginContext



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

    def run(self):
        raise PluginBaseException("Plugin Base 'run' must be overriden by Plugin")

    def requests_ui_element(self, element_id: str):
        return self.plugin_context.requests_ui_element(element_id)

    def message(self, event: BaseEvent):
        return self.plugin_context.message(event)

    def message_to(self, name: str, event: BaseEvent):
        return self.plugin_context.message_to(name, event)

    def message_to_selected(self, names: list[str], event: BaseEvent):
        return self.plugin_context.message_to_selected(names, event)

    def emit(self, event_type: str, data: tuple = ()):
        self.plugin_context.emit(event_type, data)

    def emit_and_await(self, event_type: str, data: tuple = ()):
        self.plugin_context.emit_and_await(event_type, data)
