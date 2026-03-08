# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types
from libs.dto.states import SourceViewStates

from plugins.plugin_types import PluginCode

from .telescope import Telescope



telescope = Telescope()



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.FocusedViewEvent):
            ...
        elif isinstance(event, Code_Event_Types.AddedNewFileEvent):
            telescope.list_box.add_row(event)
        elif isinstance(event, Code_Event_Types.RemovedFileEvent):
            telescope.list_box.remove_row(event)
        elif isinstance(event, Code_Event_Types.FilePathSetEvent):
            telescope.list_box.update_label(event)

    def load(self):
        window = self.request_ui_element("main-window")

        telescope.map_parent_resize_event(window)
        telescope.set_transient_for(window)
        telescope.set_emit(self.emit)

        event  = Event_Factory.create_event("register_command",
            command_name = "telescope",
            command      = Handler,
            binding_mode = "released",
            binding      = "<Control>b"
        )
        self.emit_to("source_views", event)

        event  = Event_Factory.create_event(
            "create_source_view",
            state = SourceViewStates.INDEPENDENT
        )
        self.emit_to("source_views", event)

        source_view = event.response
        telescope.set_source_view(source_view)

        event       = Event_Factory.create_event(
            "register_completer",
            completer = source_view.get_completion()
        )
        self.emit_to("completion", event)


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
        telescope.set_active_row( view.get_buffer() )
        telescope.hide() if telescope.is_visible() else telescope.show()
