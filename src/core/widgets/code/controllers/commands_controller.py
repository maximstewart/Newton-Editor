# Python imports

# Lib imports

# Application imports
from libs.dto.code import (
    CodeEvent,
    GetCommandSystemEvent,
    FocusedViewEvent
)

from ..command_system import CommandSystem

from .controller_base import ControllerBase



class CommandsController(ControllerBase, list):
    def __init__(self):
        super(CommandsController, self).__init__()


    def _controller_message(self, event: CodeEvent):
        if isinstance(event, GetCommandSystemEvent):
            event.response = self.get_command_system()

    def get_command_system(self):
        command_system         = CommandSystem()
        command_system.emit    = self.emit
        command_system.emit_to = self.emit_to

        self.append(command_system)

        return command_system
