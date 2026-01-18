# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports
from ..base_event import BaseEvent



@dataclass
class CodeEvent(BaseEvent):
    ignore_focus: bool = False
    view: any          = None
    file: any          = None
    next_file: any     = None
    buffer: any        = None
    response: any      = None
