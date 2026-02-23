# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource
from gi.repository import Gio

# Application imports
from ..command_helpers import update_info_bar_if_focused



def execute(
    view: GtkSource.View,
    uri: str
):
    logger.debug("Command: DnD Load File To Buffer")
    file = view.command.new_file(view)

    gfile  = Gio.File.new_for_uri(uri)
    view.command.exec_with_args(
        "load_file",
        (view, gfile, file)
    )

    view.set_buffer(file.buffer)

    update_info_bar_if_focused(view.command, view)
