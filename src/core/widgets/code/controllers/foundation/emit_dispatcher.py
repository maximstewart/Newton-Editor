# Python imports

# Lib imports

# Application imports
from ...event_factory import Event_Factory_Types



class EmitDispatcher:
    def __init__(self):
        super(EmitDispatcher, self).__init__()


    def emit(self, event: Event_Factory_Types.CodeEvent):
        self.message_all(event)

    def emit_to(self, controller: str, event: Event_Factory_Types.CodeEvent):
        self.message_to(controller, event)
