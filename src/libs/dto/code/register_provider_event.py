# Python imports
from dataclasses import dataclass, field

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from ..base_event import BaseEvent



@dataclass
class RegisterProviderEvent(BaseEvent):
    provider_name: str                     = ""
    provider: GtkSource.CompletionProvider = None
    language_ids: list                     = field(default_factory=lambda: [])
