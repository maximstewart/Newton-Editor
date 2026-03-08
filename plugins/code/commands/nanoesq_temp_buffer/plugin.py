# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .cut_to_temp_buffer import Handler
from .paste_temp_buffer import Handler2



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        ...

    def load(self):
        event = Event_Factory.create_event("register_command",
            command_name = "cut_to_temp_buffer",
            command      = Handler,
            binding_mode = "held",
            binding      = "<Control>k"
        )

        self.emit_to("source_views", event)

        event = Event_Factory.create_event("register_command",
            command_name = "paste_temp_buffer",
            command      = Handler2,
            binding_mode = "held",
            binding      = "<Control>u"
        )

        self.emit_to("source_views", event)

    def run(self):
        ...
