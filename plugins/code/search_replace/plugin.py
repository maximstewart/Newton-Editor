# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .search_replace import SearchReplace



search_replace = SearchReplace()



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.FocusedViewEvent):
            self._handle_view_change(event)

    def _handle_view_change(self, event: Code_Event_Types.FocusedViewEvent):
        if search_replace.is_visible():
            buffer = search_replace.active_view.get_buffer()
            search_replace.clear_highlight(buffer)

        search_replace.active_view = event.view

        if search_replace.is_visible():
            search_replace._find_entry_search_change(
                search_replace.find_entry
            )

    def load(self):
        footer = self.requests_ui_element("footer-container")
        footer.add( search_replace )

        event = Event_Factory.create_event("register_command",
            command_name = "search_replace",
            command      = Handler,
            binding_mode = "released",
            binding      = "<Control>f"
        )

        self.message_to("source_views", event)

    def run(self):
        ...
 

class Handler:
    @staticmethod
    def execute(
        view: any
    ):
        logger.debug("Command: Search/Replace")

        search_replace.hide() if search_replace.is_visible() else search_replace.show()
