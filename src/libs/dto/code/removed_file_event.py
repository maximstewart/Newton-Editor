# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports
from .code_event import CodeEvent



@dataclass
class RemovedFileEvent(CodeEvent):
    fname: str = ""
    fpath: str = ""
    ftype: str = ""
