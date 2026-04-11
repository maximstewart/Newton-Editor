# Python imports

# Lib imports

# Application imports
from libs.controllers.controller_base import ControllerBase
from libs.event_factory import Event_Factory, Code_Event_Types

from .dto.code.events import \
    RegisterLspClientEvent, UnregisterLspClientEvent
from .dto.code.lsp.lsp_message_structs import \
    LSPResponseTypes, LSPResponseRequest, LSPResponseNotification

from .ui_manager import UIManager

from .provider import Provider
from .provider_response_cache import ProviderResponseCache
from .client_manager import ClientManager
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
        self.client_manager: ClientManager         = ClientManager()
        self.response_registry: ResponseRegistry   = ResponseRegistry()

    def _load_widgets(self):
        self.ui_manager: LSPManagerUI = UIManager()
        self.ui_manager.connect('create-client', self._on_create_client)
        self.ui_manager.connect('close-client', self._on_close_client)

    def _do_bind_mapping(self):
        self.response_cache.set_lsp_manager_client(self.client_manager)
        self.provider.response_cache = self.response_cache
        self.response_registry.set_event_hub(
            self.emit, self.emit_to, self.provider
        )

    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.RegisterLspClientEvent):
            self.response_registry.register_handler(event.lang_id, event.handler)
            self.ui_manager.add_client_listing(event.lang_id, event.lang_config)
        elif isinstance(event, Code_Event_Types.UnregisterLspClientEvent):
            self.response_registry.unregister_handler(event.lang_id)
            self.ui_manager.remove_client_listing(event.lang_id)

    def _on_create_client(self, ui, lang_id: str, workspace_path: str) -> bool:
        init_opts = ui.get_init_opts(lang_id)
        result    = self.create_client(
            lang_id,
            workspace_path,
            init_opts,
            ui.adddress_entry.get_text(),
            f"{ int( ui.adddress_port.get_value() ) }"
        )

        if result:
            ui.toggle_client_buttons(show_close = True)

        return result

    def _on_close_client(self, ui, lang_id: str) -> bool:
        result = self.close_client(lang_id)

        if result:
            ui.toggle_client_buttons(show_close = False)

        return result

    def handle_destroy(self):
        self.ui_manager.disconnect_by_func(self._on_create_client)
        self.ui_manager.disconnect_by_func(self._on_close_client)

    def create_client(
        self,
        lang_id: str,
        workspace_path: str,
        init_opts: dict[str, str],
        address: str,
        port: str
    ) -> bool:
        client  = self.client_manager.create_client(
            lang_id, workspace_path, init_opts, address, port
        )
        handler = self.response_registry.get_handler(lang_id)
        self.client_manager.active_language_id = lang_id

        if not client or not handler:
            logger.error(f"LSP Manager: Either 'client' or 'handler' didn't get created...'")
            self.close_client(lang_id)
            return False

        handler.set_context(self.response_registry)
        handler.set_response_cache(self.response_cache)

        client.handle_lsp_response = self.server_response

        return True

    def close_client(self, lang_id: str) -> bool:
        self.client_manager.close_client(lang_id)
        self.response_registry.close_handler(lang_id)

        return True

    def server_response(self, lsp_response: LSPResponseTypes | dict):
        logger.debug(f"LSP Response: { lsp_response }")

        if isinstance(lsp_response, dict):
            if not self.client_manager.active_language_id in self.client_manager.clients:
                logger.debug(f"No LSP client for '{self.client_manager.active_language_id}', skipping 'server_response'")
                return

            controller = self.client_manager.get_active_client()
            if "type" in lsp_response and lsp_response["type"] == "connected":
                controller.send_initialize_message()

            return

        if isinstance(lsp_response, LSPResponseRequest):
            if not self.client_manager.active_language_id in self.client_manager.clients:
                logger.debug(f"No LSP client for '{self.client_manager.active_language_id}', skipping 'server_response'")
                return

            controller = self.client_manager.get_active_client()
            event      = controller.get_event_by_id(lsp_response.id)
            handler    = self.response_registry.get_handler(
                self.client_manager.active_language_id, event
            )

            if not handler: return
            handler.handle(event, lsp_response.result, controller)
        elif isinstance(lsp_response, LSPResponseNotification):
            handler = self.response_registry.get_handler("default", lsp_response.method)

            if not handler: return

            handler.set_context(self.response_registry)
            handler.set_response_cache(self.response_cache)
            handler.handle(lsp_response.method, lsp_response.params, None)
