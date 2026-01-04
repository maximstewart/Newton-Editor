# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource
from gi.repository import Gio

# Application imports



def execute(
    view: GtkSource.View,
    uri: str
):
    logger.debug("DnD Load File To Buffer Command")

    buffer = view.get_buffer()
    file   = view.files_manager.get_file(buffer)

    if not file.ftype == "buffer":
        file = view.command.exec("new_file")

    gfile  = Gio.File.new_for_uri(uri)
    view.command.exec_with_args(
        "load_file",
        (view, gfile, file)
    )

    has_focus = view.command.exec("has_focus")
    if has_focus:
        view.command.exec("update_info_bar")
