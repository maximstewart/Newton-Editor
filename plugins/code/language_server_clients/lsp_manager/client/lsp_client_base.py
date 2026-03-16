# Python imports

# Lib imports

# Application imports
from ..dto.code.lsp.lsp_message_structs import ClientRequest, ClientNotification

from .lsp_client_events import LSPClientEvents



class LSPClientBase(LSPClientEvents):
    def _send_message(self, data: ClientRequest or ClientNotification):
        raise NotImplementedError

    def start_client(self):
        raise NotImplementedError

    def stop_client(self):
        raise NotImplementedError
