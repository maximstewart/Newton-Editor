# Python imports
from concurrent.futures import ThreadPoolExecutor
import asyncio
from asyncio import Queue

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from libs.dto.code.lsp.lsp_message_structs import LSPResponseTypes, LSPResponseRequest, LSPResponseNotification

from core.widgets.code.completion_providers.provider_response_cache_base import ProviderResponseCacheBase

from .controllers.lsp_controller import LSPController
from .mixins.lsp_client_events_mixin import LSPClientEventsMixin
from .mixins.lsp_server_events_mixin import LSPServerEventsMixin



class ProviderResponseCache(LSPClientEventsMixin, LSPServerEventsMixin, ProviderResponseCacheBase):
    def __init__(self):
        super(ProviderResponseCache, self).__init__()

        self.executor       = ThreadPoolExecutor(max_workers = 1)
        self.matchers: dict = {}
        self.clients: dict  = {}
        self._cache_refresh_timeout_id: int = None
        self._last_active_language_id: str  = None


    def create_client(
        self,
        lang_id: str = "python",
        workspace_uri: str = "",
        init_opts: dict = {
    }) -> bool:
        if lang_id in self.clients: return False

        address                        = "127.0.0.1"
        port                           = 9999
        uri                            = f"ws://{address}:{port}/{lang_id}"
        controller                     = LSPController()
        controller.handle_lsp_response = self.server_response

        controller.set_language(lang_id)
        controller.set_socket(uri)
        controller.start_client()

        if not controller.ws_client.wait_for_connection(timeout = 5.0):
            logger.error(f"Failed to connect to LSP server for {lang_id}")
            return False

        self.clients[lang_id] = controller
        controller.send_initialize_message(init_opts, "", f"file://{workspace_uri}")

        return True

    def close_client(self, lang_id: str) -> bool:
        if lang_id not in self.clients: return False

        controller = self.clients.pop(lang_id)
        controller.stop_client()

        return True

    # TODO: Need to map 'lang_id' to a given language response class and 
    #       pass the controller to a 'server_response' method there.
    #       It would allow clean separation of each language's idiosyncracies 
    def server_response(self, lsp_response: LSPResponseTypes):
        logger.debug(f"LSP Response: { lsp_response }")

        if isinstance(lsp_response, LSPResponseRequest):
            if not self._last_active_language_id in self.clients:
                logger.debug(f"No LSP client for '{self._last_active_language_id}', skipping 'server_response'")
                return
            
            controller = self.clients[self._last_active_language_id]
            event      = controller.get_event_by_id(lsp_response.id)

            match event:
                case "textDocument/completion":
                    self._handle_completion_response(lsp_response.result)
                case "textDocument/definition":
                    result = lsp_response.result
                    if not result: return
                    uri    = result[0]["uri"]
                    if "jdt://" in uri:
                        controller._lsp_java_class_file_contents(uri)
                        return

                    self._handle_definition_response(uri, result[0]["range"])
                case "java/classFileContents":
                    self._handle_java_class_file_contents(lsp_response.result)
                case _:
                    ...
        elif isinstance(lsp_response, LSPResponseNotification):
            match lsp_response.method:
                case "textDocument/publishDiagnostics":
                    ...
                case _:
                    ...

    def filter(self, word: str) -> list[dict]:
        return []

    def filter_with_context(self, context: GtkSource.CompletionContext)  -> list[dict]:
        response = []
        iter     = self.get_iter_correctly(context)
        iter.backward_char()
        char_str = iter.get_char()

        if char_str == "." or char_str == " ":
            for label, item in self.matchers.items():
                response.append(item)

            return response

        word = self.get_word(context).rstrip()
        for label, item in self.matchers.items():
            if label.startswith(word):
                response.append(item)

        return response
