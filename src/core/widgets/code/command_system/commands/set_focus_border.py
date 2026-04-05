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
    logger.debug("Command: Set Focus Border")
    ctx = view.get_parent().get_style_context()
    ctx.add_class("source-view-focused")

    lview = view.sibling_left
    while lview is not None:
        ctx = lview.get_parent().get_style_context()
        ctx.remove_class("source-view-focused")
        lview = lview.sibling_left

    rview = view.sibling_right
    while rview is not None:
        ctx = rview.get_parent().get_style_context()
        ctx.remove_class("source-view-focused")
        rview = rview.sibling_right
