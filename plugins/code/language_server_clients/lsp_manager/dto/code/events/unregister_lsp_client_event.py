# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports
from .lsp_event import LspEvent



@dataclass
class UnregisterLspClientEvent(LspEvent):
    lang_id: str = ""
