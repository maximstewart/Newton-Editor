# Python imports
from dataclasses import dataclass

# Lib imports

# Application imports
from .code_event import CodeEvent
from libs.dto.states.source_view_states import SourceViewStates



@dataclass
class RemoveSourceViewEvent(CodeEvent):
    ...
