# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource
from gi.repository import Gio

# Application imports
from libs.dto.code import FocusedViewEvent

from ..source_file import SourceFile



def execute(
    view: GtkSource.View,
):
    logger.debug("Command: Set MiniView")
    event_system.emit("set-mini-view", (view,))
