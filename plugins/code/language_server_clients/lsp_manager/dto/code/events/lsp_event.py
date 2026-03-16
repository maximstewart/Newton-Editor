# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports
from libs.dto.code.events import CodeEvent



@dataclass
class LspEvent(CodeEvent):
    ...
