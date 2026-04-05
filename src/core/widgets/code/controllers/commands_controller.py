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
        if isinstance(event, Code_Event_Types.CreateCommandSystemEvent):
            event.response = self.create_command_system()
        elif isinstance(event, Code_Event_Types.RemovedSourceViewEvent):
            self.remove_command_system(event)

    def create_command_system(self):
        command_system         = SourceViewCommandSystem()
        command_system.emit    = self.emit
        command_system.emit_to = self.emit_to

        self.append(command_system)

        return command_system

    def remove_command_system(self, event: Code_Event_Types.RemovedSourceViewEvent):
        self.remove(event.view.command)
