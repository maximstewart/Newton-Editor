# Python imports

# Lib imports

# Application imports
from libs.controllers.controller_base import ControllerBase

from libs.event_factory import Code_Event_Types

from ..command_system import SourceViewCommandSystem



class CommandsController(ControllerBase, list):
    def __init__(self):
        super(CommandsController, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.GetNewCommandSystemEvent):
            event.response = self.get_new_command_system()

    def get_new_command_system(self):
        command_system         = SourceViewCommandSystem()
        command_system.emit    = self.emit
        command_system.emit_to = self.emit_to

        self.append(command_system)

        return command_system
