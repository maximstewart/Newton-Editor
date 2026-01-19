# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports


@dataclass
class Requests:
    bind_keys: list = field(default_factory = lambda: [])
