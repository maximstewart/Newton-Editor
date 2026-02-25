# Python imports
from dataclasses import dataclass, field

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from ..base_event import BaseEvent



@dataclass
class RegisterCommandEvent(BaseEvent):
    command_name: str    = ""
    command: callable    = None
    binding_mode: str    = ""
    binding: str or list = ""
