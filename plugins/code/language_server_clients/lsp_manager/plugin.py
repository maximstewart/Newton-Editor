# Python imports

# Lib imports
import gi

from gi.repository import GLib

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types
from libs.dto.states import SourceViewStates

from plugins.plugin_types import PluginCode

from .dto.code import events as lsp_events
from .commands import Commands
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

        lsp_manager.ui_manager.map_parent_resize_event(window)

        self._manage_signals("register_command")

        self._manage_provider("register_provider")

        event  = Event_Factory.create_event(
            "create_source_view",
            state = SourceViewStates.INDEPENDENT
        )
        self.emit_to("source_views", event)

        scrolled_win, source_view = event.response
        lsp_manager.ui_manager.set_source_view(scrolled_win, source_view)

    def unload(self):
        Event_Factory.unregister_events( lsp_events.__dict__.items() )

        self.unregister_controller("lsp_manager")

        window = self.request_ui_element("main-window")

        lsp_manager.ui_manager.unmap_parent_resize_event(window)

        self._manage_signals("unregister_command")

        self._manage_provider("unregister_provider")

        lsp_manager.handle_destroy()

    def _manage_signals(self, action: str):
        _commands             = Commands
        _commands.lsp_manager = lsp_manager

        event = Event_Factory.create_event(action,
            command_name = "lsp_manager_toggle",
            command      = _commands.lsp_manager_toggle,
            binding_mode = "released",
            binding      = "<Shift><Control>l"
        )
        self.emit_to("source_views", event)

        event = Event_Factory.create_event(action,
            command_name = "lsp_references",
            command      = _commands.lsp_references,
            binding_mode = "released",
            binding      = "<Control>i"
        )
        self.emit_to("source_views", event)

        event = Event_Factory.create_event(action,
            command_name = "lsp_implementation",
            command      = _commands.lsp_implementation,
            binding_mode = "released",
            binding      = "<Shift><Control>i"
        )
        self.emit_to("source_views", event)

        event = Event_Factory.create_event(action,
            command_name = "lsp_definition",
            command      = _commands.lsp_definition,
            binding_mode = "released",
            binding      = "<Control>g"
        )
        self.emit_to("source_views", event)

    def _manage_provider(self, action: str):
        event = Event_Factory.create_event(
            action,
            provider_name = "LSP Completer",
            provider      = lsp_manager.provider,
            language_ids  = []
        )
        self.emit_to("completion", event)

    def run(self):
        ...

    def generate_plugin_element(self):
        ...
