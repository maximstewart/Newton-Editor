# Python imports
import json
import enum
from dataclasses import dataclass

# Lib imports

# Application imports
from .lsp_structs import TextDocumentItem



class MessageEncoder(json.JSONEncoder):
    """
    Encodes an object in JSON
    """

    def default(self, o):  # pylint: disable=E0202
        return o.__dict__


@dataclass
class ClientRequest(object):
    def __init__(self, id: int, method: str, params: dict):
        """
        Constructs a new Client Request instance.

        :param int id: Message id to track instance.
        :param str method: The type of lsp request being made.
        :param dict params: The arguments of the given method.
        """
        self.jsonrpc = "2.0"
        self.id      = id
        self.method  = method
        self.params  = params

@dataclass
class ClientNotification(object):
    def __init__(self, method: str, params: dict):
        """
        Constructs a new Client Notification instance.

        :param str method: The type of lsp notification being made.
        :param dict params: The arguments of the given method.
        """
        self.jsonrpc = "2.0"
        self.method  = method
        self.params  = params

@dataclass
class LSPResponseRequest(object):
        """
        Constructs a new LSP Response Request instance.

        :param id result: The id of the given message.
        :param dict result: The arguments of the given method.
        """
        jsonrpc: str
        id: int
        result: dict

@dataclass
class LSPResponseNotification(object):
        """
        Constructs a new LSP Response Notification instance.

        :param str method: The type of lsp notification being made.
        :params dict result: The arguments of the given method.
        """
        jsonrpc: str
        method: str
        params: dict

@dataclass
class LSPIDResponseNotification(object):
        """
        Constructs a new LSP Response Notification instance.

        :param str method: The type of lsp notification being made.
        :params dict result: The arguments of the given method.
        """
        jsonrpc: str
        id: int
        method: str
        params: dict


class MessageTypes(ClientRequest, ClientNotification, LSPResponseRequest, LSPResponseNotification, LSPIDResponseNotification):
    ...

class ClientMessageTypes(ClientRequest, ClientNotification):
    ...

class LSPResponseTypes(LSPResponseRequest, LSPResponseNotification):
    ...
