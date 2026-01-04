# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GLib
from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Paste Temp Buffer Command")

    view.clear_temp_cut_buffer_delayed()

    buffer     = view.get_buffer()
    itr        = buffer.get_iter_at_mark( buffer.get_insert() )
    insert_itr = itr.copy()

    buffer.insert(insert_itr, view._cut_buffer, -1)

    view.set_temp_cut_buffer_delayed()
