# Python imports

# Lib imports

# Application imports
from ..event_factory import Event_Factory_Types

from ..command_system import CommandSystem

from .foundation.controller_base import ControllerBase



class CommandsController(ControllerBase, list):
    def __init__(self):
        super(CommandsController, self).__init__()


    def _controller_message(self, event: Event_Factory_Types.CodeEvent):
        if isinstance(event, Event_Factory_Types.GetCommandSystemEvent):
            event.response = self.get_command_system()

    def get_command_system(self):
        command_system         = CommandSystem()
        command_system.emit    = self.emit
        command_system.emit_to = self.emit_to

        self.append(command_system)

        return command_system
