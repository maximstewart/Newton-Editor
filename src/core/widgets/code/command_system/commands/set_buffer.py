# Python imports


# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from ...source_file import SourceFile
from ..command_helpers import update_info_bar_if_focused



def execute(
    view: GtkSource.View,
    file: SourceFile
):
    logger.debug("Command: Set Buffer")

    if not file:
        view.command.new_file(view)
        return

    view.set_buffer(file.buffer)

    update_info_bar_if_focused(view.command, view)

