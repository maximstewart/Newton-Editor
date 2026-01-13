# Python imports

# Lib imports

# Application imports
from ..event_factory import Event_Factory_Types



class ControllerContextException(Exception):
    ...



class ControllerContext:
    def __init__(self):
        super(ControllerContext, self).__init__()


    def message_to(self, name: str, event: Event_Factory_Types.CodeEvent):
        raise ControllerContextException("Controller Context 'message_to' must be overriden by Controller Manager...")

    def message_all(self, event: Event_Factory_Types.CodeEvent):
        raise ControllerContextException("Controller Context 'message_all' must be overriden by Controller Manager...")
