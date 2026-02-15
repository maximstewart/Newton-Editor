# Python imports
from enum import Enum

# Lib imports

# Application imports



class SourceViewStates(Enum):
    INSERT      = 0
    MULTIINSERT = 1
    COMMAND     = 2
    READONLY    = 3
