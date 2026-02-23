# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports
from .code_event import CodeEvent



@dataclass
class FileExternallyModifiedEvent(CodeEvent):
    ...
