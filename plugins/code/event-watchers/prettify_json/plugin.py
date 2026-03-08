# Python imports

# Lib imports
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .prettify_json import add_prettify_json



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.PopulateSourceViewPopupEvent):
            language = event.buffer.get_language()
            if not language: return

            if "json" == language.get_id():
                add_prettify_json(event.buffer, event.menu)

    def load(self):
        ...

    def run(self):
        ...
