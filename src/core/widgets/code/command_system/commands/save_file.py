# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from ..command_helpers import set_language_and_style



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Command: Save File")
    file   = view.command.get_file(view)
    buffer = file.buffer

    if file.ftype == "buffer":
        file.save_as()
        set_language_and_style(view, file)
        return

    file.save()

