# Python imports

# Lib imports

# Application imports
from .lsp_client_events import LSPClientEvents
from libs.dto.code.lsp.lsp_message_structs import ClientRequest, ClientNotification



class LSPClientBase(LSPClientEvents):
    def _send_message(self, data: ClientRequest or ClientNotification):
        raise NotImplementedError

    def start_client(self):
        raise NotImplementedError

    def stop_client(self):
        raise NotImplementedError
