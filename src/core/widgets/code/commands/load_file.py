# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource
from gi.repository import Gio

# Application imports
from ..source_file import SourceFile



def execute(
    view: GtkSource.View,
    gfile: Gio.File,
    file: SourceFile = None,
):
    logger.debug("Load File Command")
    if not file:
        file = view.files_manager.new()

    file.load_path(gfile)

    language   = view.language_manager \
                       .guess_language(file.fname, None)
    file.ftype = language

    file.buffer.set_language(language)
    file.buffer.set_style_scheme(view.syntax_theme)
