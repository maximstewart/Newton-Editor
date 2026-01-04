# Python imports


# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from ..source_file import SourceFile



def execute(
    view: GtkSource.View,
    file: SourceFile
):
    logger.debug("Set Buffer Command")

    buffer = view.get_buffer()
    _file  = view.files_manager.get_file(buffer)
    _file.remove_observer(view)

    if not file:
        view.command.exec("new_file")
        return

    view.set_buffer(file.buffer)
    file.add_observer(view)

    has_focus = view.command.exec("has_focus")
    if has_focus:
        view.command.exec("update_info_bar")

