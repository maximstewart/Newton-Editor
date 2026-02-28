# Python imports

# Lib imports

# Application imports
from ..singleton_raised import SingletonRaised

from ..dto.base_event import BaseEvent

from .emit_dispatcher import EmitDispatcher
from .controller_message_bus import ControllerMessageBus



class ControllerBaseException(Exception):
    ...



class ControllerBase(SingletonRaised, EmitDispatcher):
    def __init__(self):
        super(ControllerBase, self).__init__()

        self.controller_message_bus: ControllerMessageBus = None


    def _controller_message(self, event: BaseEvent):
        raise ControllerBaseException("Controller Base '_controller_message' must be overridden...")

    def set_controller_message_bus(self, controller_message_bus: ControllerMessageBus):
        self.controller_message_bus = controller_message_bus

    def message(self, event: BaseEvent):
        return self.controller_message_bus.message(event)

    def message_to(self, name: str, event: BaseEvent):
        return self.controller_message_bus.message_to(name, event)

    def message_to_selected(self, names: list[str], event: BaseEvent):
        for name in names:
            self.controller_message_bus.message_to_selected(name, event)

    def register_controller(self, name: str, controller):
        self.controller_message_bus.register_controller(name, controller)
