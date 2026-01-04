# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Buffer Undo Command")

    buffer       = view.get_buffer()
    undo_manager = buffer.get_undo_manager()

    if undo_manager.can_undo():
        buffer.undo()
