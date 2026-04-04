# Python imports

# Lib imports
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

# Application imports
from ...mixins.mark_support_mixin import MarkSupportMixin



class MarkerManager(MarkSupportMixin):

    def __init__(self):
        super().__init__()

        self.buffer_markers: dict = {}

        self.selection_tag: Gtk.TextTag = Gtk.TextTag.new("selection")
        self.selection_tag.props.background = "rgba(111, 168, 220, 0.64)"
        self.selection_tag.props.foreground = "#ffffff"


    def move_by_char(self, buffer, is_forward: bool, is_selection: bool):
        self._move(buffer, is_forward, is_selection, mode = "char")

    def move_by_word(self, buffer, is_forward: bool, is_selection: bool):
        self._move(buffer, is_forward, is_selection, mode = "word")

    def move_by_line(self, buffer, is_forward: bool, is_selection: bool):
        self._move(buffer, is_forward, is_selection, mode = "line")

    def _move(self, buffer, is_forward: bool, is_selection: bool, mode: str):
        self.clear_highlight(buffer)
        self.insert_selection_tag(buffer)

        for mark_hash in self.buffer_markers:
            marker        = self.buffer_markers[mark_hash]
            start_mark    = marker["start_mark"]
            end_mark      = marker["end_mark"]
            has_selection = marker["is_selection"]

            start_itr     = buffer.get_iter_at_mark(start_mark)
            end_itr       = buffer.get_iter_at_mark(end_mark)

            self._proc_move(
                buffer, is_forward, is_selection, mode, mark_hash,
                start_mark, end_mark, has_selection, start_itr, end_itr
            )

    def _proc_move(
        self, buffer, is_forward: bool, is_selection: bool, mode: str,
        mark_hash, start_mark, end_mark, has_selection, start_itr, end_itr
    ):
        if is_selection:
            if mark_hash:
                self.buffer_markers[mark_hash]["is_selection"] = True

            self._move_iter(buffer, end_itr, mode, is_forward)
            buffer.move_mark(end_mark, end_itr)

            self._apply_selection(buffer, start_itr, end_itr)
            return

        if has_selection:
            caret_itr     = buffer.get_iter_at_mark(end_mark)
            start_itr     = buffer.get_iter_at_mark(start_mark)
            is_left_edge  = caret_itr.compare(start_itr) <= 0
            is_right_edge = not is_left_edge
            can_move      = (
                (is_forward and is_right_edge) or
                (not is_forward and is_left_edge)
            )

            self.collapse_selection(buffer, mark_hash, start_mark, end_mark, is_forward)
            if mode == "word":
                if not can_move: return

                itr = caret_itr
                self._move_iter(buffer, itr, mode, is_forward)
                buffer.move_mark(start_mark, itr)
                buffer.move_mark(end_mark, itr)

            return

        # No selection - move both anchor and caret together
        self._move_iter(buffer, end_itr, mode, is_forward)

        buffer.move_mark(start_mark, end_itr)
        buffer.move_mark(end_mark, end_itr)

    def collapse_selection(self,
        buffer, mark_hash, start_mark, end_mark, is_forward: bool
    ):
        if mark_hash:
            self.buffer_markers[mark_hash]["is_selection"] = False

        start_itr = buffer.get_iter_at_mark(start_mark)
        end_itr   = buffer.get_iter_at_mark(end_mark)

        # Determine which side is visually the caret
        if start_itr.compare(end_itr) <= 0:
            left  = start_itr
            right = end_itr
        else:
            left  = end_itr
            right = start_itr

        # If moving forward -> collapse to right edge
        collapse_itr = right if is_forward else left

        buffer.move_mark(start_mark, collapse_itr)
        buffer.move_mark(end_mark, collapse_itr)

    def move_along_word(self, itr: Gtk.TextIter, count: int):
        def not_is_word(ch: str):
            return not is_word(ch)

        def is_word(ch: str):
            return ch and (ch.isalnum() or ch == "_")

        def is_special(ch: str):
            return ch in "-"

        def is_punct(ch: str):
            return ch in ".;?!"

        def step(fwd: bool):
            return itr.forward_cursor_position() if fwd else itr.backward_cursor_position()

        def peek(fwd: bool):
            if fwd: return itr.get_char()
            tmp = itr.copy()
            return tmp.backward_cursor_position() and tmp.get_char()

        def walk(fwd, cond: callable):
            while True:
                ch = peek(fwd)
                if not cond(ch): break
                if not step(fwd): return False

            return True

        fwd = count > 0
        for _ in range( abs(count) ):
            ch = peek(fwd)

            if is_special(ch) or is_punct(ch):
                step(fwd)
            elif is_word(ch):
                if not walk(fwd, is_word): return
            else:
                if not walk(fwd, not_is_word): return
                if not walk(fwd, is_word): return

    def _move_iter(self, buffer, itr_, mode: str, is_forward: bool):
        if mode == "char":
            itr_.forward_char() if is_forward else itr_.backward_char()
        elif mode == "word":
            self.move_along_word(itr_, 1 if is_forward else -1)
        elif mode == "line":
            line   = itr_.get_line()
            offset = itr_.get_line_offset()

            max_line = buffer.get_line_count() - 1
            new_line = line + 1 if is_forward else line - 1
            new_line = max(0, min(max_line, new_line))

            itr_.set_line(new_line)
            self.move_to_offset(offset, itr_)

    def _apply_selection(self, buffer, start_itr, end_itr):
        if start_itr.compare(end_itr) <= 0:
            buffer.apply_tag(self.selection_tag, start_itr, end_itr)
        else:
            buffer.apply_tag(self.selection_tag, end_itr, start_itr)


    def button_release_event(self, source_view, event):
        buffer = source_view.get_buffer()

        coords = source_view.window_to_buffer_coords(
            Gtk.TextWindowType.TEXT,
            event.x,
            event.y,
        )

        is_over_text, target_itr, _ = source_view.get_iter_at_position(
            coords.buffer_x,
            coords.buffer_y,
        )

        if not is_over_text:
            target_itr.forward_visible_line()
            target_itr.backward_char()

        if self.remove_mark_set(target_itr, buffer):
            return

        self.insert_mark_set(target_itr, buffer)

    def key_press_event(self, source_view, event, key_mapper):
        ...
