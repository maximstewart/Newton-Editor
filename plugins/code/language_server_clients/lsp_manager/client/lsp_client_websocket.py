# Python imports

# Lib imports
from gi.repository import GLib

# Application imports
# from libs import websockets
from ..dto.code.lsp.lsp_messages import get_message_str, get_message_obj
from ..dto.code.lsp.lsp_message_structs import           \
    LSPResponseTypes, ClientRequest, ClientNotification, \
    LSPResponseRequest, LSPResponseNotification, LSPIDResponseNotification

from .lsp_client_base import LSPClientBase
from .websocket import Websocket



class LSPClientWebsocket(LSPClientBase):
    def _send_message(self, data: ClientRequest | ClientNotification):
        if not data: return

        message_str  = get_message_str(data)
        message_size = len(message_str)
        message      = f"Content-Length: {message_size}\r\n\r\n{message_str}"

        logger.debug(f"Client: {message_str}")
        self.websocket.send(message_str)

    def start_client(self):
        self.websocket = Websocket()
        self.websocket.set_socket(self._socket)
        self.websocket.set_callback(self._monitor_lsp_response)
        self.websocket.start_client()

        return self.websocket

    def stop_client(self):
        if not hasattr(self, "websocket"): return
        self.websocket.close_client()

    def _monitor_lsp_response(self, data: dict | None):
        if not data: return {}

        message      = get_message_obj(data)
        keys         = message.keys()
        lsp_response = data

        if "result" in keys:
            lsp_response = LSPResponseRequest(**get_message_obj(data))

        if "method" in keys:
            lsp_response = LSPResponseNotification(**get_message_obj(data)) if not "id" in keys else LSPIDResponseNotification( **get_message_obj(data) )

        if isinstance(lsp_response, str):
            lsp_response = get_message_obj(lsp_response)

        GLib.idle_add(self.handle_lsp_response, lsp_response)
