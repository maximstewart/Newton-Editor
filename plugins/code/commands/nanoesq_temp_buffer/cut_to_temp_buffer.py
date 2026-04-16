# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from .helpers import clear_temp_cut_buffer_delayed, set_temp_cut_buffer_delayed



class Handler:
    @staticmethod
    def execute(view: GtkSource.View, *args, **kwargs):
        logger.debug("Command: Cut to Temp Buffer")

        clear_temp_cut_buffer_delayed(view)

        buffer = view.get_buffer()

        if buffer.get_has_selection():
            start_itr, end_itr = buffer.get_selection_bounds()

            start_itr.set_line_offset(0)

            if not end_itr.ends_line():
                end_itr.forward_to_line_end()

            if not end_itr.is_end():
                end_itr.forward_char()
        else:
            itr = buffer.get_iter_at_mark(buffer.get_insert())

            start_itr = itr.copy()
            start_itr.set_line_offset(0)

            end_itr = start_itr.copy()
            if not end_itr.forward_line():
                end_itr = buffer.get_end_iter()

        if not hasattr(view, "_cut_buffer"):
            view._cut_buffer = ""

        text = buffer.get_text(start_itr, end_itr, True)

        if not text.endswith("\n"):
            text += "\n"

        view._cut_buffer += text

        buffer.delete(start_itr, end_itr)
        buffer.place_cursor(start_itr)

        set_temp_cut_buffer_delayed(view)