# Python imports
from dataclasses import dataclass, field

# Lib imports
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

# Application imports
from .code_event import CodeEvent



@dataclass
class PopulateSourceViewPopupEvent(CodeEvent):
    menu: Gtk.Widget = None
