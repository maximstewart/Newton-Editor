# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Command: Duplicate Line")

    buffer = view.get_buffer()

    if not buffer.get_has_selection():
        had_selection = False
        itr        = buffer.get_iter_at_mark( buffer.get_insert() )
        start_itr  = itr.copy()
        end_itr    = itr.copy()
        start_line = itr.get_line() + 1
        start_char = itr.get_line_offset()
    else:
        had_selection = True
        start_itr, end_itr = buffer.get_selection_bounds()
        sline      = start_itr.get_line()
        eline      = end_itr.get_line()
        start_line = eline + 1
        start_char = start_itr.get_line_offset()
        end_char   = end_itr.get_line_offset()
        range_line_size  = eline - sline

    start_itr.backward_visible_line()
    start_itr.forward_line()
    end_itr.forward_line()
    end_itr.backward_char()

    line_str = buffer.get_slice(start_itr, end_itr, True)
    end_itr.forward_char()
    buffer.insert(end_itr, f"{line_str}\n", -1)

    if not had_selection:
        new_itr = buffer.get_iter_at_line_offset(start_line, start_char)
        buffer.place_cursor(new_itr)
    else:
        new_itr     = buffer.get_iter_at_line_offset(start_line, start_char)
        new_end_itr = buffer.get_iter_at_line_offset((start_line + range_line_size), end_char)
        buffer.select_range(new_itr, new_end_itr)
