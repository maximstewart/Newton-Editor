# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports
from .code_event import CodeEvent



@dataclass
class CursorMovedEvent(CodeEvent):
    line: int  = 0
    char: int  = 0
