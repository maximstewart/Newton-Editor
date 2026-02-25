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
    logger.debug("Command: Buffer Redo")

    buffer       = view.get_buffer()
    undo_manager = buffer.get_undo_manager()

    if undo_manager.can_redo():
        buffer.redo()
