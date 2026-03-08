# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types
from libs.dto.states import SourceViewStates

from plugins.plugin_types import PluginCode

from .lsp_manager import LSPManager



lsp_manager = LSPManager()



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        ...

    def load(self):
        window = self.request_ui_element("main-window")

        lsp_manager.map_parent_resize_event(window)

        event  = Event_Factory.create_event("register_command",
            command_name = "LSP Manager",
            command      = Handler,
            binding_mode = "released",
            binding      = ["<Shift><Control>l", "<Control>g", "<Control>i"]
        )
        self.emit_to("source_views", event)

        event = Event_Factory.create_event(
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
        lsp_manager.load_lsp_servers_config()
        lsp_manager.set_source_view(source_view)
        lsp_manager.load_lsp_servers_config_placeholders()
        lsp_manager.provider.response_cache.emit = self.emit
        lsp_manager.provider.response_cache.emit_to = self.emit_to
        lsp_manager.provider.response_cache._prompt_completion_request = self._prompt_completion_request

    def run(self):
        ...

    def generate_plugin_element(self):
        ...

    def _prompt_completion_request(self):
        event  = Event_Factory.create_event(
            "get_active_view",
        )
        self.emit_to("source_views", event)
        view = event.response

        event  = Event_Factory.create_event(
            "request_completion",
            view     = view,
            provider = lsp_manager.provider
        )
        self.emit_to("completion", event)


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
                lsp_manager.provider.response_cache.process_goto_definition(
                    file.ftype, file.fpath, line, column
                )

                return

            if char_str == "i":
                return

        lsp_manager.hide() if lsp_manager.is_visible() else lsp_manager.show()
