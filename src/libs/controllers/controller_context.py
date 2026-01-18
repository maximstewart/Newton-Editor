# Python imports

# Lib imports

# Application imports
from ..dto.base_event import BaseEvent



class ControllerContextException(Exception):
    ...



class ControllerContext:
    def __init__(self):
        super(ControllerContext, self).__init__()


    def message_to(self, name: str, event: BaseEvent):
        raise ControllerContextException("Controller Context 'message_to' must be overriden by Controller Manager...")

    def message_all(self, event: BaseEvent):
        raise ControllerContextException("Controller Context 'message_all' must be overriden by Controller Manager...")
