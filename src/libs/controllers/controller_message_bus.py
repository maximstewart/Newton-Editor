# Python imports

# Lib imports

# Application imports
from ..dto.base_event import BaseEvent



class ControllerMessageBusException(Exception):
    ...



class ControllerMessageBus:
    def __init__(self):
        super(ControllerMessageBus, self).__init__()


    def message(self, event: BaseEvent):
        raise ControllerMessageBusException("Controller Message Bus 'message' must be overriden by Controller Manager...")

    def message_to(self, name: str, event: BaseEvent):
        raise ControllerMessageBusException("Controller Message Bus 'message_to' must be overriden by Controller Manager...")

    def message_to_selected(self, name: list, event: BaseEvent):
        raise ControllerMessageBusException("Controller Message Bus 'message_to_selected' must be overriden by Controller Manager...")

    def register_controller(self, name: str, controller):
        raise ControllerMessageBusException("Controller Message Bus 'register_controller' must be overriden by Controller Manager...")

    def unregister_controller(self, name: str):
        raise ControllerMessageBusException("Controller Message Bus 'unregister_controller' must be overriden by Controller Manager...")
