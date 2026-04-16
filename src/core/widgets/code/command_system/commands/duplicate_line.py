# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(view: GtkSource.View, *args, **kwargs):
    logger.debug("Command: Duplicate Line")

    buffer = view.get_buffer()

    if buffer.get_has_selection():
        start_itr, \
        end_itr    = buffer.get_selection_bounds()
        start_line = start_itr.get_line()
        end_line   = end_itr.get_line()
        scol       = start_itr.get_line_offset()
        ecol       = end_itr.get_line_offset()
    else:
        itr        = buffer.get_iter_at_mark(buffer.get_insert())
        start_line = end_line = itr.get_line()
        col        = itr.get_line_offset()

    start_itr = buffer.get_iter_at_line(start_line)
    end_itr   = buffer.get_iter_at_line(end_line)

    if not end_itr.ends_line():
        end_itr.forward_to_line_end()

    if not end_itr.is_end():
        end_itr.forward_char()

    text       = buffer.get_text(start_itr, end_itr, True)
    insert_itr = buffer.get_iter_at_line(end_line)

    insert_itr.forward_to_line_end()
    if not insert_itr.is_end():
        insert_itr.forward_char()

    buffer.insert(insert_itr, text)

    if buffer.get_has_selection():
        new_start = buffer.get_iter_at_line_offset(end_line + 1, scol)
        new_end   = buffer.get_iter_at_line_offset(end_line + 1 + (end_line - start_line), ecol)
        buffer.select_range(new_start, new_end)
    else:
        new_start = buffer.get_iter_at_line_offset(end_line + 1, col)
        buffer.place_cursor(new_start)
