# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View,
    *args,
    **kwargs
):
    logger.debug("Command: Focus Left Sibling")
    if not view.sibling_left: return
    view.sibling_left.get_parent().show()
    view.sibling_left.grab_focus()
