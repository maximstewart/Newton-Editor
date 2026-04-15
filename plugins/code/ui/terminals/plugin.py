# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .terminals_view import TerminalsView



terminals_view = TerminalsView()



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        ...

    def load(self):
        terminals_view.emit_to = self.emit_to
        footer                 = self.request_ui_element("footer-container")
        footer.add( terminals_view )

        self._manage_signals("register_command")

    def unload(self):
        self._manage_signals("unregister_command")
        terminals_view.destroy()

    def _manage_signals(self, action: str):
        event = Event_Factory.create_event(action,
            command_name = "terminals",
            command      = Handler,
            binding_mode = "released",
            binding      = "<Control>."
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
        logger.debug("Command: Terminal")
        terminals_view.set_code_view(view)

        terminals_view.hide() if terminals_view.is_visible() else terminals_view.show()
