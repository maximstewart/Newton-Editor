# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GLib

# Application imports
from ..command_helpers import update_info_bar_if_focused



def execute(
    view: GtkSource.View,
    uri: str,
    *args,
    **kwargs
):
    logger.debug("Command: DnD Load File To Buffer")
    file  = view.command.new_file(view)
    gfile = Gio.File.new_for_uri(uri)

    view.command.exec_with_args(
        "load_file",
        view, gfile, file
    )

    view.set_buffer(file.buffer)

    update_info_bar_if_focused(view.command, view)
    view.emit("focus-in-event", Gdk.Event())

    def scroll_to_insert_itr(view):
        buffer = view.get_buffer()
        itr    = buffer.get_iter_at_mark( buffer.get_insert() )
        view.scroll_to_iter(itr, 0.2, False, 0, 0)

    GLib.idle_add(scroll_to_insert_itr, view)

