# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from ..command_helpers import set_language_and_style, update_info_bar_if_focused



def execute(
    view: GtkSource.View,
    *args,
    **kwargs
):
    logger.info("Command: Save File As")
    file   = view.command.get_file(view)
    buffer = file.buffer

    file.save_as()

    set_language_and_style(view, file)

    update_info_bar_if_focused(view.command, view)
