# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .provider import Provider



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()

        self.provider: Provider = None


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        ...

    def load(self):
        self.provider = Provider()

        event = Event_Factory.create_event(
            "register_provider",
            provider_name = "Snippets Completer",
            provider      = self.provider,
            language_ids  = []
        )
        self.emit_to("completion", event)

    def run(self):
        ...
