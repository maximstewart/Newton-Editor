# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource
from gi.repository import Gio

# Application imports
from ...source_file import SourceFile
from ..command_helpers import set_language_and_style



def execute(
    view: GtkSource.View,
    gfile: Gio.File,
    file: SourceFile = None,
):
    logger.debug("Command: Load File")
    if not file:
        file = view.command.new_file(view)

    file.load_path(gfile)

    set_language_and_style(view, file)
