# Python imports

# Lib imports

# Application imports
from libs.dto.base_event import BaseEvent



class PluginContextException(Exception):
    ...



class PluginContext:
    """ PluginContext """

    def __init__(self):
        super(PluginContext, self).__init__()

    def requests_ui_element(self, element_id: str):
        raise PluginContextException("Plugin Context 'requests_ui_element' must be overridden...")

    def _controller_message(self, event: BaseEvent):
        raise PluginContextException("Plugin Context '_controller_message' must be overridden...")

    def message(self, event: BaseEvent):
        raise PluginContextException("Plugin Context 'message' must be overridden...")

    def message_to(self, name: str, event: BaseEvent):
        raise PluginContextException("Plugin Context 'message_to' must be overridden...")

    def message_to_selected(self, names: list[str], event: BaseEvent):
        raise PluginContextException("Plugin Context 'message_to_selected' must be overridden...")

    def emit(self, event_type: str, data: tuple = ()):
        raise PluginContextException("Plugin Context 'emit' must be overridden...")

    def emit_and_await(self, event_type: str, data: tuple = ()):
        raise PluginContextException("Plugin Context 'emit_and_await' must be overridden...")

    def register_controller(self, name: str, controller):
        raise PluginContextException("Plugin Context 'register_controller' must be overridden...")

