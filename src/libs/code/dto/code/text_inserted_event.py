# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports
from .code_event import CodeEvent



@dataclass
class TextInsertedEvent(CodeEvent):
    line: int  = 0
    char: int  = 0
    value: str = ""
