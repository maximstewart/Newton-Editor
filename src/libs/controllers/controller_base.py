# Python imports

# Lib imports

# Application imports
from ..singleton import Singleton

from ..dto.base_event import BaseEvent

from .emit_dispatcher import EmitDispatcher
from .controller_context import ControllerContext



class ControllerBaseException(Exception):
    ...



class ControllerBase(Singleton, EmitDispatcher):
    def __init__(self):
        super(ControllerBase, self).__init__()

        self.controller_context: ControllerContext = None


    def _controller_message(self, event: BaseEvent):
        raise ControllerBaseException("Controller Base '_controller_message' must be overridden...")

    def set_controller_context(self, controller_context: ControllerContext):
        self.controller_context = controller_context

    def message(self, event: BaseEvent):
        return self.controller_context.message(event)

    def message_to(self, name: str, event: BaseEvent):
        return self.controller_context.message_to(name, event)

    def message_to_selected(self, names: list[str], event: BaseEvent):
        for name in names:
            self.controller_context.message_to_selected(name, event)

    def register_controller(self, name: str, controller):
        self.controller_context.register_controller(name, controller)
