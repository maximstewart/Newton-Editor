# Python imports


# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from ..command_helpers import set_language_and_style, update_info_bar_if_focused



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Command: New File")

    file = view.command.new_file(view)
    set_language_and_style(view, file)

    view.set_buffer(file.buffer)

    update_info_bar_if_focused(view.command, view)
    return file
