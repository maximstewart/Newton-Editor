# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View,
    *args,
    **kwargs
):
    logger.debug("Command: Cut to Temp Buffer")

    view.clear_temp_cut_buffer_delayed()

    buffer     = view.get_buffer()
    itr        = buffer.get_iter_at_mark( buffer.get_insert() )
    start_itr  = itr.copy()
    end_itr    = itr.copy()
    start_line = itr.get_line() + 1
    start_char = itr.get_line_offset()

    start_itr.backward_visible_line()
    start_itr.forward_line()
    end_itr.forward_line()

    line_str   = buffer.get_slice(start_itr, end_itr, True)
    view._cut_buffer += f"{line_str}"
    buffer.delete(start_itr, end_itr)

    view.set_temp_cut_buffer_delayed()
