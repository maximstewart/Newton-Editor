# Python imports
from os import path

# Lib imports
import gi

from gi.repository import GLib

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .response_handler import PythonHandler


class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        ...

    def load(self):
        dirPth = path.dirname( path.realpath(__file__) ) 
        with open(f"{dirPth}/config/lsp-server-config.json", "r") as f:
            config = f.read()
            event  = Event_Factory.create_event("register_lsp_client",
                lang_id     = "python",
                lang_config = config,
                handler     = PythonHandler
            )
            self.emit_to("lsp_manager", event)

    def run(self):
        ...
