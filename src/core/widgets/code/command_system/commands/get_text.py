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
    logger.debug("Command: Get Text")

    buffer = view.get_buffer()
    start_itr, end_itr = buffer.get_bounds()
    return buffer.get_text(start_itr, end_itr, True)
