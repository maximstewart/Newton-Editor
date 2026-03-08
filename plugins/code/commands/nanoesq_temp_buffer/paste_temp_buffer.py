# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GLib
from gi.repository import GtkSource

# Application imports
from .helpers import clear_temp_cut_buffer_delayed, set_temp_cut_buffer_delayed


class Handler2:
    @staticmethod
    def execute(
        view: GtkSource.View,
        *args,
        **kwargs
    ):
        logger.debug("Command: Paste Temp Buffer")
        if not hasattr(view, "_cut_temp_timeout_id"): return
        if not hasattr(view, "_cut_buffer"): return
        if not view._cut_buffer: return

        clear_temp_cut_buffer_delayed(view)

        buffer     = view.get_buffer()
        itr        = buffer.get_iter_at_mark( buffer.get_insert() )
        insert_itr = itr.copy()

        buffer.insert(insert_itr, view._cut_buffer, -1)

        set_temp_cut_buffer_delayed(view)
