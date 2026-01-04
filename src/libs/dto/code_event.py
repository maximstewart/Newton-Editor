# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports
from .observable_event import ObservableEvent



@dataclass
class CodeEvent(ObservableEvent):
    etype: str         = ""
    ignore_focus: bool = False
    view: any          = None
    file: any          = None
    next_file: any     = None
    buffer: any        = None