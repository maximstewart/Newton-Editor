# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()

    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        ...

    def load(self):
        event = Event_Factory.create_event("register_command",
            command_name = "toggle_source_view",
            command      = Handler,
            binding_mode = "released",
            binding      = "<Shift><Control>h"
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
        logger.debug("Command: Toggle Source View")
        target = view.get_parent()
        target.hide() if target.is_visible() else target.show()

        if view.sibling_left:
            target = view.sibling_left.get_parent()
            target.show()
            view.sibling_left.grab_focus()

        if view.sibling_right:
            target = view.sibling_right.get_parent()
            target.show()
            view.sibling_right.grab_focus()

