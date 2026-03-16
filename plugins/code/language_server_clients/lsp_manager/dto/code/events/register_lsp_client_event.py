# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports
from ....response_handlers.base_handler import BaseHandler 

from .lsp_event import LspEvent



@dataclass
class RegisterLspClientEvent(LspEvent):
    lang_id: str         = ""
    lang_config: str     = "{}"
    handler: BaseHandler = None
