# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View,
    style: str
):
    logger.debug("Set Buffer Style Command")

    buffer = editor.get_buffer()
    buffer.set_style_scheme(
        view.style_scheme_manager.get_scheme(style)
    )
