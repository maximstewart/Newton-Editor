# Python imports
import threading
from os import path
import json

# Lib imports
import gi
from gi.repository import GLib

# Application imports
from libs.dto.code.lsp.lsp_messages import get_message_str
from libs.dto.code.lsp.lsp_message_structs import LSPResponseTypes, ClientRequest, ClientNotification
from .lsp_controller_websocket import LSPControllerWebsocket



class LSPController(LSPControllerWebsocket):
    def __init__(self):
        super(LSPController, self).__init__()

        # https://github.com/microsoft/multilspy/tree/main/src/multilspy/language_servers
        # initialize-params-slim.json was created off of jedi_language_server one
        # self._init_params   = settings_manager.get_lsp_init_data()

        self._language: str                 = ""
        self._init_params: dict             = {}
        self._event_history: dict[int, str] = {}

        try:
            _USER_HOME  = path.expanduser('~')
            _SCRIPT_PTH = path.dirname( path.realpath(__file__) )
            _LSP_INIT_CONFIG = f"{_SCRIPT_PTH}/../configs/initialize-params-slim.json"

            with open(_LSP_INIT_CONFIG) as file:
                data = file.read().replace("{user.home}", _USER_HOME)
                self._init_params = json.loads(data)
        except Exception as e:
            logger.error( f"LSP Controller: {_LSP_INIT_CONFIG}\n\t\t{repr(e)}" )

        self._message_id: int = -1
        self._socket          = None
        self.read_lock        = threading.Lock()
        self.write_lock       = threading.Lock()

    def set_language(self, language: str):
        self._language = language

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
