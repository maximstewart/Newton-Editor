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
        if not isinstance(event, Code_Event_Types.FocusedViewEvent): return
        event = Event_Factory.create_event(
            "get_file", buffer = event.view.get_buffer()
        )
        self.emit_to("files", event)

        file = event.response
        if not file: return
        if file.ftype == "buffer": return

        file.check_file_on_disk()

        if file.is_deleted():
            file_is_deleted(file, self.emit)
        elif file.is_externally_modified():
            file_is_externally_modified(file, self.emit)

    def load(self):
        ...

    def unload(self):
        ...

    def run(self):
        ...
