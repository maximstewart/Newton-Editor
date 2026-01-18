# Python imports

# Lib imports

# Application imports
from ..dto.base_event import BaseEvent



class EmitDispatcher:
    def __init__(self):
        super(EmitDispatcher, self).__init__()


    def emit(self, event: BaseEvent):
        self.message(event)

    def emit_to(self, controller: str, event: BaseEvent):
        self.message_to(controller, event)
