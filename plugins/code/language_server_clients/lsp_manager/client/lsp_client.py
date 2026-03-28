# Python imports
import threading
from os import path
import json

# Lib imports
import gi
from gi.repository import GLib

# Application imports
from ..dto.code.lsp.lsp_messages import get_message_str
from ..dto.code.lsp.lsp_message_structs import \
    LSPResponseTypes, ClientRequest, ClientNotification
from .lsp_client_websocket import LSPClientWebsocket



class LSPClient(LSPClientWebsocket):
    def __init__(self):
        super(LSPClient, self).__init__()

        self._language: str                 = ""
        self._workspace_path: str           = ""
        self._init_params: dict             = {}
        self._init_opts: dict               = {}

        try:
            _USER_HOME  = path.expanduser('~')
            _SCRIPT_PTH = path.dirname( path.realpath(__file__) )
            _LSP_INIT_CONFIG = f"{_SCRIPT_PTH}/../configs/initialize-params-slim.json"

            with open(_LSP_INIT_CONFIG) as file:
                data = file.read()
                self._init_params = json.loads(data)
        except Exception as e:
            logger.error( f"LSP Controller: {_LSP_INIT_CONFIG}\n\t\t{repr(e)}" )


        self._socket                        = None
        self._message_id: int               = -1
        self._event_history: dict[int, str] = {}

        self.read_lock                      = threading.Lock()
        self.write_lock                     = threading.Lock()


    def set_language(self, language: str):
        self._language = language

    def set_workspace_path(self, workspace_path: str):
        self._workspace_path = workspace_path

    def set_init_opts(self, init_opts: dict[str, str]):
        self._init_opts = init_opts

    def set_socket(self, socket: str):
        self._socket = socket

    def unset_socket(self):
        self._socket = None

    def send_notification(self, method: str, params: dict = {}):
        self._send_message( ClientNotification(method, params) )

    def send_request(self, method: str, params: dict = {}):
        self._message_id += 1
        self._event_history[self._message_id] = method
        self._send_message( ClientRequest(self._message_id, method, params) )

    def get_event_by_id(self, message_id: int) -> str:
        if not message_id in self._event_history: return
        return self._event_history[message_id]

    def handle_lsp_response(self, lsp_response: LSPResponseTypes):
        raise NotImplementedError
