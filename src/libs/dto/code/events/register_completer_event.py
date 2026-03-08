# Python imports
from dataclasses import dataclass, field

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from .code_event import CodeEvent



@dataclass
class RegisterCompleterEvent(CodeEvent):
    completer: GtkSource.Completion = None
