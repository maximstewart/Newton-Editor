# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports
from .code_event import CodeEvent



@dataclass
class FocusedViewEvent(CodeEvent):
    left_view: any  = False
    right_view: any = False
