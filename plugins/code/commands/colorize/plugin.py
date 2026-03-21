# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .colorize import Colorize



colorize = Colorize()



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.AddedNewFileEvent):
            colorize.handle_colorize(event.file.buffer)
        elif isinstance(event, Code_Event_Types.TextChangedEvent):
            colorize.handle_colorize(event.buffer)

    def load(self):
        self._manage_signals("register_command")

    def unload(self):
        self._manage_signals("unregister_command")
        event = Event_Factory.create_event("get_source_views")

        self.emit_to("source_views", event)
        for view in event.response:
            buffer = view.get_buffer()
            colorize.clear_color_tags(buffer)

    def _manage_signals(self, action: str):
        event = Event_Factory.create_event(action,
            command_name = "tggle_colorize",
            command      = Handler,
            binding_mode = "released",
            binding      = "<Shift><Control>c"
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
        logger.debug("Command: Toggle Colorize")

        colorize.is_colorize_paused = not colorize.is_colorize_paused
        if colorize.is_colorize_paused:
            colorize.clear_color_tags( view.get_buffer() )
            return

        colorize.handle_colorize( view.get_buffer() )

