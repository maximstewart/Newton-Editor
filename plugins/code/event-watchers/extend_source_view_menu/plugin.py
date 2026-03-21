# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .source_view_menu import extend_source_view_menu



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()

    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.PopulateSourceViewPopupEvent):
            extend_source_view_menu(event.buffer, event.menu)

    def load(self):
        ...

    def unload(self):
        ...

    def run(self):
        ...
