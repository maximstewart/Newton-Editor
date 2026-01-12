# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from ..command_helpers import update_info_bar_if_focused



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Command: Open File(s)")
    gfiles = event_system.emit_and_await("open-files")
    if not gfiles: return

    file = view.command.get_file(view)
    if file.ftype == "buffer":
        gfile = gfiles.pop()
        view.command.exec_with_args("load_file", (view, gfile, file))
        view.set_buffer(file.buffer)
        update_info_bar_if_focused(view.command, view)

    for i, gfile in enumerate(gfiles):
        view.command.exec_with_args("load_file", (view, gfile))
