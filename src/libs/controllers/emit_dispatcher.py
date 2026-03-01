# Python imports

# Lib imports

# Application imports
from ..dto.base_event import BaseEvent



class EmitDispatcher:
    """
        EmitDispatcher is used for allowing controllers to pass/hook in
        their message system to children that need to signal events.
        Note how we are not handling return info from the 'message' methods
        whereas a controller would or could do so.
    """

    def __init__(self):
        super(EmitDispatcher, self).__init__()


    def emit(self, event: BaseEvent):
        self.message(event)

    def emit_to(self, controller: str, event: BaseEvent):
        self.message_to(controller, event)

    def emit_to_selected(self, names: list[str], event: BaseEvent):
        self.message_to_selected(names, event)
