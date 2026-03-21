# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .commenter import Commenter



commenter = Commenter()



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        ...

    def load(self):
        event = Event_Factory.create_event("register_command",
            command_name = "keyboard_tggl_comment",
            command      = Handler,
            binding_mode = "released",
            binding      = "<Control>slash"
        )

        self.emit_to("source_views", event)

    def unload(self):
        event = Event_Factory.create_event("unregister_command",
            command_name = "keyboard_tggl_comment",
            command      = Handler,
            binding_mode = "released",
            binding      = "<Control>slash"
        )

        self.emit_to("source_views", event)

    def run(self):
        ...


class Handler:
    @staticmethod
    def execute(
        view: any,
        *args,
        **kwargs
    ):
        logger.debug("Command: Toggle Comment")
        commenter.keyboard_tggl_comment( view.get_buffer() )