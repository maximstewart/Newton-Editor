# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .autopairs import Autopairs



autopairs = Autopairs()



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()

    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        ...

    def load(self):
        event = Event_Factory.create_event("register_command",
            command_name = "autopairs",
            command      = Handler,
            binding_mode = "held",
            binding      = [
                "'", "`", "[", "]",
                '<Shift>"',
                '<Shift>(',
                '<Shift>)',
                '<Shift>{',
                '<Shift>}'
            ]
        )

        self.message_to("source_views", event)

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
        logger.debug("Command: Autopairs")
        autopairs.handle_word_wrap(view.get_buffer(), char_str)
