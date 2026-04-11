# Python imports
from concurrent.futures import ThreadPoolExecutor

# Lib imports

# Application imports
from .config import get_lsp_connect_timout
from .mixins.client_manager_events_mixin import ClientManagerEventsMixin
from .client.lsp_client import LSPClient



class ClientManager(ClientManagerEventsMixin):
    def __init__(self):
        super(ClientManager, self).__init__()

        self._cache_refresh_timeout_id: int = None

        self.executor: ThreadPoolExecutor   = ThreadPoolExecutor(max_workers = 1)
        self.active_language_id: str        = ""
        self.clients: dict                  = {}


    def create_client(
        self,
        lang_id: str,
        workspace_path: str,
        init_opts: dict[str, str],
        address: str = "127.0.0.1",
        port: str    = "9999"
    ) -> LSPClient:
        if lang_id in self.clients: return None

        uri     = f"ws://{address}:{port}/{lang_id}?workspace={workspace_path}"
        client  = LSPClient()

        client.set_socket(uri)
        client.set_language(lang_id)
        client.set_workspace_path(workspace_path)
        client.set_init_opts(init_opts)
        client.start_client()

        if not client.websocket.wait_for_connection(timeout = get_lsp_connect_timout()):
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
