# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .telescope import Telescope



telescope = Telescope()



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.FocusedViewEvent):
            ...

    def load(self):
        window = self.request_ui_element("main-window")
        telescope.set_transient_for(window)

        event = Event_Factory.create_event("register_command",
            command_name = "telescope",
            command      = Handler,
            binding_mode = "released",
            binding      = "<Control>b"
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
        logger.debug("Command: Telescope")

        telescope.hide() if telescope.is_visible() else telescope.show()
