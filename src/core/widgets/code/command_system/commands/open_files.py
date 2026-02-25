# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from ..command_helpers import update_info_bar_if_focused



def execute(
    view: GtkSource.View,
    *args,
    **kwargs
):
    logger.debug("Command: Open File(s)")
    file       = view.command.get_file(view)
    start_path = None 
    if not file.ftype == "buffer":
        start_path = file.get_location()

    gfiles = event_system.emit_and_await("open-files", (None, None, start_path))
    if not gfiles: return

    if file.ftype == "buffer":
        gfile = gfiles.pop()
        view.command.exec_with_args("load_file", view, gfile, file)
        view.set_buffer(file.buffer)
        update_info_bar_if_focused(view.command, view)

    for i, gfile in enumerate(gfiles):
        view.command.exec_with_args("load_file", view, gfile)
