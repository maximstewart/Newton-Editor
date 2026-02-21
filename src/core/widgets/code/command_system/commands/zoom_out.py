# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource
from gi.repository import Pango

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Command: Zoom Out")

    ctx = view.get_style_context()
    if view.zoom_level > 1:
        view.zoom_level -= 1

        font_desc        = \
            Pango.FontDescription(f"Monospace {view.zoom_level}")

        view.modify_font(font_desc)
