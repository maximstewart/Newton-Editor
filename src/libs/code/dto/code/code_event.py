# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports



@dataclass
class CodeEvent:
    ignore_focus: bool = False
    view: any          = None
    file: any          = None
    next_file: any     = None
    buffer: any        = None
    response: any      = None
