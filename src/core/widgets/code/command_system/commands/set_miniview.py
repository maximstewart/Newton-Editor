# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View,
):
    logger.debug("Command: Set MiniView")
    event_system.emit("set-mini-view", (view,))
