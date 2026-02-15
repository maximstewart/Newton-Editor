# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from libs.dto.base_event import BaseEvent
from libs.event_factory import Event_Factory

from plugins.plugin_types import PluginCode

from .provider import Provider



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()

        self.provider: Provider = None


    def _controller_message(self, event: BaseEvent):
        ...

    def load(self):
        self.provider = Provider()

        event = Event_Factory.create_event(
            "register_provider",
            provider_name = "Example Completer",
            provider      = self.provider,
            language_ids  = []
        )
        self.message_to("completion", event)

    def run(self):
        ...
