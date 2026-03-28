# Python imports
from dataclasses import dataclass, field
from dataclasses import asdict

# Gtk imports

# Application imports
from .requests import Requests



@dataclass
class Manifest:
    name: str          = ""
    author: str        = ""
    description: str   = ""
    version: str       = "0.0.1"
    support: str       = "support@mail.com"
    credit: str        = ""
    copyright: str     = "GPLv2"
    pre_launch: bool   = False
    autoload: bool     = True
    requests: Requests = field(default_factory = lambda: Requests())

    def __post_init__(self):
        if isinstance(self.requests, dict):
            self.requests = Requests(**self.requests)

    def as_dict(self):
        return asdict(self)
