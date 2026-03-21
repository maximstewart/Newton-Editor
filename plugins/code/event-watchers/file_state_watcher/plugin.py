# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .watcher_checks import *



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.TextChangedEvent):
            event.file.check_file_on_disk()

            if event.file.is_deleted():
                file_is_deleted(event, self.emit)
            elif event.file.is_externally_modified():
                file_is_externally_modified(event, self.emit)

    def load(self):
        ...

    def unload(self):
        ...

    def run(self):
        ...
