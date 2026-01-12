# Python imports

# Lib imports

# Application imports
from libs.singleton import Singleton

from libs.dto.code.code_event import CodeEvent

from .controller_base import ControllerBase
from .controller_context import ControllerContext



class ControllerManagerException(Exception):
    ...



class ControllerManager(Singleton, dict):
    def __init__(self):
        super(ControllerManager, self).__init__()


    def _crete_controller_context(self) -> ControllerContext:
        controller_context             = ControllerContext()
        controller_context.message_to  = self.message_to
        controller_context.message_all = self.message_all

        return controller_context

    def register_controller(self, name: str, controller: ControllerBase):
        if not name or controller == None:
            raise ControllerManagerException("Must pass in a 'name' and 'controller'...")

        controller.set_controller_context(
            self._crete_controller_context()
        )

        self[name] = controller


    def message_to(self, name: str, event: CodeEvent):
        self[name]._controller_message(event)

    def message_all(self, event: CodeEvent):
        for key in self.keys():
            self[key]._controller_message(event)
