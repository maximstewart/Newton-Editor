# Python imports
from concurrent.futures import ThreadPoolExecutor

# Lib imports

# Application imports
from .mixins.lsp_client_events_mixin import LSPClientEventsMixin
from .client.lsp_client import LSPClient



class LSPManagerClient(LSPClientEventsMixin):
    def __init__(self):
        super(LSPManagerClient, self).__init__()

        self._cache_refresh_timeout_id: int = None

        self.executor: ThreadPoolExecutor   = ThreadPoolExecutor(max_workers = 1)
        self.active_language_id: str        = ""
        self.clients: dict                  = {}


    def create_client(
        self,
        lang_id: str = "python",
        workspace_uri: str = "",
        init_opts: dict = {}
    ) -> LSPClient:
        if lang_id in self.clients: return None

        address = "127.0.0.1"
        port    = 9999
        uri     = f"ws://{address}:{port}/{lang_id}"
        client  = LSPClient()

        client.set_language(lang_id)
        client.set_socket(uri)
        client.start_client()

        if not client.ws_client.wait_for_connection(timeout = 5.0):
            logger.error(f"Failed to connect to LSP server for {lang_id}")
            return None

        self.clients[lang_id] = client

        return client

    def close_client(self, lang_id: str) -> bool:
        if lang_id not in self.clients: return False

        controller = self.clients.pop(lang_id)
        controller.stop_client()

        return True

    def get_active_client(self) -> LSPClient:
        return self.clients[self.active_language_id]
