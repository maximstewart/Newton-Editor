# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode



history: list     = []
history_size: int = 30


class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.RemovedFileEvent):
            if event.file.ftype == "buffer": return

            if len(history) == history_size:
                history.pop(0)

            history.append(event.file.fpath)

    def load(self):
        self._manage_signals("register_command")

    def unload(self):
        self._manage_signals("unregister_command")

    def _manage_signals(self, action: str):
        event = Event_Factory.create_event(action,
            command_name = "file_history_pop",
            command      = Handler,
            binding_mode = "released",
            binding      = "<Shift><Control>t"
        )

        self.emit_to("source_views", event)

    def run(self):
        ...


class Handler:
    @staticmethod
    def execute(
        view: any,
        char_str: str,
        *args,
        **kwargs
    ):
        logger.debug("Command: File History")
        if len(history) == 0: return

        view._on_uri_data_received(
            [
                f"file://{history.pop()}"
            ]
        )
