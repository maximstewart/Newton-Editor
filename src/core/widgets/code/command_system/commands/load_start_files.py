# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource
from gi.repository import Gio

# Application imports



def execute(
    view: GtkSource.View,
    *args,
    **kwargs
):
    logger.debug("Command: Load Start File(s)")

    starting_files = settings_manager.get_starting_files()

    if not starting_files: return

    file   = starting_files.pop()
    file   = file.replace("FILE|", "")
    gfile  = Gio.File.new_for_path(file)
    file   = view.command.get_file(view)

    view.command.exec_with_args(
        "load_file",
        view, gfile, file
    )

    if not starting_files: return

    for file in starting_files:
        file  = file.replace("FILE|", "")
        gfile = Gio.File.new_for_path(file)

        view.command.exec_with_args("load_file", view, gfile)
