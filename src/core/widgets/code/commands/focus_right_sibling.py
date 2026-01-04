# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Focus Right Sibling Command")
    if not view.sibling_right: return
    view.sibling_right.grab_focus()
