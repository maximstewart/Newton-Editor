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
    logger.debug("Command: Move To Left Sibling")
    if not view.sibling_left: return

    buffer = view.get_buffer()
    popped_file, next_file = view.command.get_swap_file(view)

    view.sibling_left.set_buffer(buffer)
    view.sibling_left.grab_focus()

    if next_file:
        view.set_buffer(next_file.buffer)
    else:
        view.command.exec("new_file")
