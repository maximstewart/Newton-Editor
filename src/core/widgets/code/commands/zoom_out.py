# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Zoom Out Command")

    ctx = view.get_style_context()
    if view.zoom_level > 1:
        ctx.remove_class(f"px{view.zoom_level}")
        view.zoom_level -= 1
        ctx.add_class(f"px{view.zoom_level}")