# Python imports

# Lib imports

# Application imports
from ..dto.base_event import BaseEvent



class ControllerContextException(Exception):
    ...



class ControllerContext:
    def __init__(self):
        super(ControllerContext, self).__init__()


    def message(self, event: BaseEvent):
        raise ControllerContextException("Controller Context 'message' must be overriden by Controller Manager...")

    def message_to(self, name: str, event: BaseEvent):
        raise ControllerContextException("Controller Context 'message_to' must be overriden by Controller Manager...")

    def message_to_selected(self, name: list, event: BaseEvent):
        raise ControllerContextException("Controller Context 'message_to_selected' must be overriden by Controller Manager...")

    def register_controller(self, name: str, controller):
        raise ControllerContextException("Controller Context 'register_controller' must be overriden by Controller Manager...")
