# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource
from gi.repository import Gio

# Application imports
from libs.dto.code_event import CodeEvent

from ..source_file import SourceFile



def execute(
    view: GtkSource.View,
):
    logger.debug("Set MiniView  Command")
    event_system.emit("set-mini-view", (view,))

    event       = CodeEvent()
    event.etype = "focused_view_change"
    event.view  = view
    view.notify_observers(event)
