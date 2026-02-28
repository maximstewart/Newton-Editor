# Python imports
import random

# Lib imports
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

# Application imports



class MarkSupportMixin:
    def clear_mark_sets(self, source_view):
        buffer = source_view.get_buffer()
        self.clear_highlight(buffer)

        for mark_set in self.buffer_markers.values():
            start_mark, end_mark, is_selection = mark_set.values()
            start_mark.set_visible(False)
            buffer.delete_mark(start_mark)
            buffer.delete_mark(end_mark)

        self.buffer_markers.clear()

    def insert_selection_tag(self, buffer):
        tag_table = buffer.get_tag_table()
        if not tag_table.lookup("selection"):
            tag_table.add(self.selection_tag)

    def clear_highlight(self, buffer):
        if not self.selection_tag: return
        start_itr, end_itr = buffer.get_bounds()
        buffer.remove_tag(self.selection_tag, start_itr, end_itr)

    def apply_to_marks(self, buffer, operation):
        buffer.block_insert_after_signal()
        buffer.begin_user_action()

        try:
            with buffer.freeze_notify():
                for mark_hash in self.buffer_markers:
                    marker        = self.buffer_markers[mark_hash]
                    start_mark    = marker["start_mark"]
                    end_mark      = marker["end_mark"]
                    has_selection = marker["is_selection"]

                    start_itr     = buffer.get_iter_at_mark(start_mark)
                    end_itr       = buffer.get_iter_at_mark(end_mark)

                    if has_selection:
                        operation(start_itr, end_itr)
                        self.collapse_selection(
                            buffer, mark_hash, start_mark, end_mark, False
                        )
                    else:
                        operation(start_itr)
        finally:
            buffer.end_user_action()
            buffer.unblock_insert_after_signal()

    def process_cursor_action(self, buffer, action):
        def remove_text(start_itr, end_itr = None):
            if end_itr:
                buffer.delete(start_itr, end_itr)
                return

            buffer.backspace(start_itr, interactive = True, default_editable = True)

        def delete_text(start_itr, end_itr = None):
            if end_itr:
                buffer.delete(start_itr, end_itr)
                return

            start_itr.forward_char()
            buffer.backspace(start_itr, interactive = True, default_editable = True)

        if action == "BACKSPACE":
            self.apply_to_marks(buffer, remove_text)
        elif action == "DELETE":
            self.apply_to_marks(buffer, delete_text)
        elif action == "ENTER":
            ...

    def move_to_offset(self, offset, start_itr):
        line_itr = start_itr.copy()

        line_itr.forward_to_line_end()

        next_line_length = line_itr.get_line_offset()
        new_offset       = min(offset, next_line_length)
        start_itr.set_line_offset(new_offset)

    def insert_mark_set(self, target_iter, buffer):
        random_bits = random.getrandbits(128)
        hash        = "%032x" % random_bits

        start_mark = Gtk.TextMark.new(
            name = f"multi-insert-start-{hash}",
            left_gravity = False
        )

        end_mark = Gtk.TextMark.new(
            name = f"multi-insert-end-{hash}",
            left_gravity = False
        )
#            left_gravity = True

        buffer.add_mark(start_mark, target_iter)
        buffer.add_mark(end_mark, target_iter)
        start_mark.set_visible(True)
        self.buffer_markers[f"{hash}"] = {
            "start_mark": start_mark,
            "end_mark": end_mark,
            "is_selection": False
        }

    def remove_mark_set(self, target_iter, buffer) -> bool:
        marks = target_iter.get_marks()

        for mark_hash in self.buffer_markers:
            start_mark, end_mark, is_selection = self.buffer_markers[mark_hash].values()
            if not start_mark in marks: continue

            start_mark.set_visible(False)
            buffer.delete_mark(start_mark)
            buffer.delete_mark(end_mark)
            del self.buffer_markers[mark_hash]

            return True

        return False
