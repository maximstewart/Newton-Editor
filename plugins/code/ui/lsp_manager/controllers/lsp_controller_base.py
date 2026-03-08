# Python imports

# Lib imports

# Application imports
from .lsp_controller_events import LSPControllerEvents
from libs.dto.code.lsp.lsp_message_structs import ClientRequest, ClientNotification



class LSPControllerBase(LSPControllerEvents):
    def _send_message(self, data: ClientRequest or ClientNotification):
        raise NotImplementedError

    def start_client(self):
        raise NotImplementedError

    def stop_client(self):
        raise NotImplementedError
