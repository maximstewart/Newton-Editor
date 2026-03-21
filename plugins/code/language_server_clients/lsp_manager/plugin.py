# Python imports

# Lib imports
import gi

from gi.repository import GLib

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types
from libs.dto.states import SourceViewStates

from plugins.plugin_types import PluginCode

from .dto.code import events as lsp_events
from .lsp_manager import LSPManager



lsp_manager = LSPManager()



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        ...

    def load(self):
        Event_Factory.register_events( lsp_events.__dict__.items() )

        self.register_controller("lsp_manager", lsp_manager)

        window = self.request_ui_element("main-window")

        lsp_manager.lsp_manager_ui.map_parent_resize_event(window)

        event  = Event_Factory.create_event("register_command",
            command_name = "LSP Manager",
            command      = Handler,
            binding_mode = "released",
            binding      = ["<Shift><Control>l", "<Control>g", "<Control>i"]
        )
        self.emit_to("source_views", event)

        event  = Event_Factory.create_event(
            "register_provider",
            provider_name = "LSP Completer",
            provider      = lsp_manager.provider,
            language_ids  = []
        )
        self.emit_to("completion", event)

        event  = Event_Factory.create_event(
            "create_source_view",
            state = SourceViewStates.INDEPENDENT
        )
        self.emit_to("source_views", event)

        source_view = event.response
        lsp_manager.lsp_manager_ui.set_source_view(source_view)

    def unload(self):
        Event_Factory.unregister_events( lsp_events.__dict__.items() )

        self.unregister_controller("lsp_manager")

        window = self.request_ui_element("main-window")

        lsp_manager.lsp_manager_ui.unmap_parent_resize_event(window)

        event  = Event_Factory.create_event("unregister_command",
            command_name = "LSP Manager",
            command      = Handler,
            binding_mode = "released",
            binding      = ["<Shift><Control>l", "<Control>g", "<Control>i"]
        )
        self.emit_to("source_views", event)

        event  = Event_Factory.create_event(
            "unregister_provider",
            provider_name = "LSP Completer"
        )
        self.emit_to("completion", event)

        lsp_manager.handle_destroy()

    def run(self):
        ...

    def generate_plugin_element(self):
        ...


class Handler:
    @staticmethod
    def execute(
        view: any,
        *args,
        **kwargs
    ):
        logger.debug("Command: LSP Manager")

        char_str = args[0]
        if char_str in ["g", "i"]:
            file   = view.command.exec("get_current_file")
            buffer = view.get_buffer()
            iter   = buffer.get_iter_at_mark( buffer.get_insert() )
            line   = iter.get_line()
            column = iter.get_line_offset()

            if char_str == "g":
                lsp_manager.lsp_manager_client.process_goto_definition(
                    file.ftype, file.fpath, line, column
                )

                return

            if char_str == "i":
                return

        lsp_manager.lsp_manager_ui.hide() if lsp_manager.lsp_manager_ui.is_visible() else lsp_manager.lsp_manager_ui.show()
