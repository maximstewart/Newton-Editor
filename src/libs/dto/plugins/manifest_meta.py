# Python imports
from dataclasses import dataclass, field
from dataclasses import asdict

# Gtk imports

# Application imports
from .manifest import Manifest



@dataclass
class ManifestMeta:
    folder: str             = ""
    path: str               = ""
    manifest: Manifest      = field(default_factory = lambda: Manifest())
    instance: object | None = None

    def as_dict(self):
        return asdict(self)
