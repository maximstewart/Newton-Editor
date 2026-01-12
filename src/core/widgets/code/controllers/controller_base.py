# Python imports

# Lib imports

# Application imports
from libs.singleton import Singleton

from libs.dto.code.code_event import CodeEvent

from .emit_dispatcher import EmitDispatcher
from .controller_context import ControllerContext



class ControllerBaseException(Exception):
    ...



class ControllerBase(Singleton, EmitDispatcher):
    def __init__(self):
        super(ControllerBase, self).__init__()

        self.controller_context: ControllerContext = None


    def _controller_message(self, event: CodeEvent):
        raise ControllerBaseException("Controller Base must override '_controller_message'...")

    def set_controller_context(self, controller_context: ControllerContext):
        self.controller_context = controller_context

    def message_to(self, name: str, event: CodeEvent):
        return self.controller_context.message_to(name, event)

    def message_all(self, event: CodeEvent):
        return self.controller_context.message_all(event)

