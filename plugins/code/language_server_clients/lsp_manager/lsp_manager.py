# Python imports

# Lib imports

# Application imports
from libs.controllers.controller_base import ControllerBase
from libs.event_factory import Event_Factory, Code_Event_Types

from .dto.code.events import \
    RegisterLspClientEvent, UnregisterLspClientEvent
from .dto.code.lsp.lsp_message_structs import \
    LSPResponseTypes, LSPResponseRequest, LSPResponseNotification

from .provider import Provider
from .provider_response_cache import ProviderResponseCache
from .lsp_manager_ui import LSPManagerUI
from .lsp_manager_client import LSPManagerClient
from .response_handlers.response_registry import ResponseRegistry



class LSPManager(ControllerBase):
    def __init__(self):
        super(LSPManager, self).__init__()

        self._init()
        self._load_widgets()
        self._do_bind_mapping()


    def _init(self):
        self.provider: Provider                    = Provider()
        self.response_cache: ProviderResponseCache = ProviderResponseCache()
        self.lsp_manager_client: LSPManagerClient  = LSPManagerClient()
        self.response_registry: ResponseRegistry   = ResponseRegistry()

    def _load_widgets(self):
        self.lsp_manager_ui: LSPManagerUI = LSPManagerUI()
        self.lsp_manager_ui.connect('create-client', self._on_create_client)
        self.lsp_manager_ui.connect('close-client', self._on_close_client)

    def _do_bind_mapping(self):
        self.response_cache.set_lsp_client(self.lsp_manager_client)
        self.provider.response_cache = self.response_cache
        self.response_registry.set_event_hub(
            self.emit, self.emit_to, self.provider
        )

    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.RegisterLspClientEvent):
            self.response_registry.register_handler(event.lang_id, event.handler)
            self.lsp_manager_ui.add_client_listing(event.lang_id, event.lang_config)
        elif isinstance(event, Code_Event_Types.UnregisterLspClientEvent):
            self.response_registry.unregister_handler(event.lang_id)

    def _on_create_client(self, ui, lang_id: str, workspace_uri: str) -> bool:
        init_opts = ui.get_init_opts(lang_id)
        result = self.create_client(lang_id, workspace_uri, init_opts)
        if result:
            ui.toggle_client_buttons(show_close=True)
        return result

    def _on_close_client(self, ui, lang_id: str) -> bool:
        result = self.close_client(lang_id)
        if result:
            ui.toggle_client_buttons(show_close=False)
        return result

    def create_client(
        self,
        lang_id: str = "python",
        workspace_uri: str = "",
        init_opts: dict = {}
    ) -> bool:
        client  = self.lsp_manager_client.create_client(
            lang_id, workspace_uri, init_opts
        )
        handler = self.response_registry.get_handler(lang_id)
        self.lsp_manager_client.active_language_id = lang_id

        if not client or not handler:
            logger.error(f"LSP Manager: Either 'client' or 'handler' didn't get created...'")
            self.close_client(lang_id)
            return False

        handler.set_context(self.response_registry)
        handler.set_response_cache(self.response_cache)

        client.handle_lsp_response = self.server_response
        client.send_initialize_message(init_opts, "", f"file://{workspace_uri}")

        return True

    def close_client(self, lang_id: str) -> bool:
        self.lsp_manager_client.close_client(lang_id)
        self.response_registry.close_handler(lang_id)

        return True

    def server_response(self, lsp_response: LSPResponseTypes):
        logger.debug(f"LSP Response: { lsp_response }")

        if isinstance(lsp_response, LSPResponseRequest):
            if not self.lsp_manager_client.active_language_id in self.lsp_manager_client.clients:
                logger.debug(f"No LSP client for '{self.lsp_manager_client.active_language_id}', skipping 'server_response'")
                return
            
            controller = self.lsp_manager_client.get_active_client()
            event      = controller.get_event_by_id(lsp_response.id)
            handler    = self.response_registry.get_handler(
                self.lsp_manager_client.active_language_id, event
            )

            if not handler: return
            handler.handle(event, lsp_response.result, controller)
        elif isinstance(lsp_response, LSPResponseNotification):
            handler = self.response_registry.get_handler("default", lsp_response.method)

            if not handler: return

            handler.set_context(self.response_registry)
            handler.set_response_cache(self.response_cache)
            handler.handle(lsp_response.method, lsp_response.params, None)
