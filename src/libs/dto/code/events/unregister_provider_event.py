# Python imports
from dataclasses import dataclass

# Lib imports

# Application imports
from .code_event import CodeEvent



@dataclass
class UnregisterProviderEvent(CodeEvent):
    provider_name: str = ""
