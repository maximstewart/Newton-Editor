# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports



@dataclass(slots = True)
class BaseEvent:
    topic: str        = None
    content: any      = None
    raw_content: any  = None
    success: callable = None
    fail: callable    = None
