# Python imports

# Lib imports

# Application imports
from libs.dto.code.code_event import CodeEvent



class EmitDispatcher:
    def __init__(self):
        super(EmitDispatcher, self).__init__()


    def emit(self, event: CodeEvent):
        self.message_all(event)

    def emit_to(self, controller: str, event: CodeEvent):
        self.message_to(controller, event)
