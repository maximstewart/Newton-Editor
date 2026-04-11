# Python imports

# Lib imports

# Application imports
from ..config import get_lsp_init_config
from ..dto.code.lsp.lsp_messages import get_message_str
from ..dto.code.lsp.lsp_message_structs import \
    LSPResponseTypes, ClientRequest, ClientNotification
from .lsp_client_websocket import LSPClientWebsocket



class LSPClient(LSPClientWebsocket):
    def __init__(self):
        super(LSPClient, self).__init__()

        self._socket: str                   = ""
        self._language: str                 = ""
        self._workspace_path: str           = ""
        self._message_id: int               = -1
        self._event_history: dict[int, str] = {}
        self._init_params: dict             = get_lsp_init_config()
        self._init_opts: dict[str, str]     = {}
        self.doc_vers: dict[str, int]       = {}


    def set_language(self, language: str):
        self._language = language

    def set_workspace_path(self, workspace_path: str):
        self._workspace_path = workspace_path

    def set_init_opts(self, init_opts: dict[str, str]):
        self._init_opts = init_opts

    def set_socket(self, socket: str):
        self._socket = socket

    def unset_socket(self):
        self._socket = ""

    def send_notification(self, method: str, params: dict = {}):
        self._send_message( ClientNotification(method, params) )

    def send_request(self, method: str, params: dict = {}):
        self._message_id += 1
        self._event_history[self._message_id] = method
        self._send_message( ClientRequest(self._message_id, method, params) )

    def get_event_by_id(self, message_id: int) -> str:
        if not message_id in self._event_history: return
        return self._event_history[message_id]

    def handle_lsp_response(self, lsp_response: LSPResponseTypes | dict):
        raise NotImplementedError
