# Python imports
from dataclasses import dataclass, field

# Lib imports
import gi
from gi.repository import Gio

# Application imports
from .code_event import CodeEvent



@dataclass
class SetInfoLabelsEvent(CodeEvent):
    info: tuple[str or Gio.File] = None
