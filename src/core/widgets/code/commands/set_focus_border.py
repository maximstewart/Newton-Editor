# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Set Focus Border Command")
    ctx = view.get_parent().get_style_context()
    ctx.add_class("source-view-focused")

    if view.sibling_right:
        ctx = view.sibling_right.get_parent().get_style_context()
    elif view.sibling_left:
        ctx = view.sibling_left.get_parent().get_style_context()

    ctx.remove_class("source-view-focused")
