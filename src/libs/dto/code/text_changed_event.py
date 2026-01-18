# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports
from .code_event import CodeEvent



@dataclass
class TextChangedEvent(CodeEvent):
    has_selection: bool = False
    start_range: int    = 0
    end_range: int      = 0
    line: int           = 0
    char: int           = 0
    value: str          = ""
