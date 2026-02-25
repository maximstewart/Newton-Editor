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
    logger.debug("Command: Close File")
    view.command.remove_file(view)
    update_info_bar_if_focused(view.command, view)
