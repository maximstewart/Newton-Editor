# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Focus Left Sibling Command")
    if not view.sibling_left: return
    view.sibling_left.grab_focus()
