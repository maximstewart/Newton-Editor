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


    def _controller_message(self, event: BaseEvent):
        raise PluginContextException("Plugin Context '_controller_message' must be overridden...")

    def request_ui_element(self, element_id: str):
        raise PluginContextException("Plugin Context 'request_ui_element' must be overridden...")

    def emit(self, event: BaseEvent):
        raise PluginContextException("Plugin Context 'emit' must be overridden...")

    def emit_to(self, name: str, event: BaseEvent):
        raise PluginContextException("Plugin Context 'emit_to' must be overridden...")

    def emit_to_selected(self, names: list[str], event: BaseEvent):
        raise PluginContextException("Plugin Context 'emit_to_selected' must be overridden...")

    def register_controller(self, name: str, controller):
        raise PluginContextException("Plugin Context 'register_controller' must be overridden...")

    def unregister_controller(self, name: str):
        raise PluginContextException("Plugin Context 'unregister_controller' must be overridden...")

