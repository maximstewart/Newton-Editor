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
    uris: list = []
):
    logger.debug("DnD Load Files Command")
    for uri in uris:
        try:
            gfile = Gio.File.new_for_uri(uri)
        except Exception as e:
            gfile = Gio.File.new_for_path(uri)

        view.command.exec_with_args("load_file", (view, gfile))