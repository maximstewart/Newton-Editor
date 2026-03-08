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

    start_path = None 
    file       = view.command.get_file(view)
    if not file.ftype == "buffer":
        start_path = file.get_location()

    gfiles = event_system.emit_and_await("open-files", (None, None, start_path))
    view._on_uri_data_received(
        [ gfile.get_uri() for gfile in gfiles ]
    )
