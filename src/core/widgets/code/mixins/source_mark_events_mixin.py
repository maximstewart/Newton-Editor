# Python imports
import random

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from libs.dto.states import SourceViewStates, MoveDirection, CursorAction



class MarkEventsMixin:
    def clear_markers(self, source_view):
        buffer = source_view.get_buffer()

        for mark in self.insert_markers:
            mark.set_visible(False)
            buffer.delete_mark(mark)

        self.insert_markers.clear()

    def _insert_mark(self, insert_iter, target_iter, buffer):
        mark_found = self._check_for_insert_marks(target_iter, buffer)

        if mark_found: return

        random_bits = random.getrandbits(128)
        hash        = "%032x" % random_bits

        mark = Gtk.TextMark.new(
            name = f"multi_insert_{hash}",
            left_gravity = False
        )

        buffer.add_mark(mark, target_iter)
        mark.set_visible(True)
        self.insert_markers.append(mark)


    def _check_for_insert_marks(self, target_iter, buffer):
        marks = target_iter.get_marks()

        for mark in marks:
            if mark in self.insert_markers[:]:
                mark.set_visible(False)
                self.insert_markers.remove(mark)
                buffer.delete_mark(mark)
                return True

        insert_itr = buffer.get_iter_at_mark( buffer.get_insert() )
        if target_iter.equal(insert_itr): return True

        return False

    def _process_cursor_action(self, buffer):
        if not self.insert_markers: return
        if self.cursor_action == CursorAction.NONE.value: return

        action = self.cursor_action
        for mark in self.insert_markers:
            itr = buffer.get_iter_at_mark(mark)

            if action == CursorAction.BACKSPACE.value:
                buffer.backspace(itr, interactive = True, default_editable = True)
            elif action == CursorAction.DELETE.value:
                itr.forward_char()
                buffer.backspace(itr, interactive = True, default_editable = True)
            elif action == CursorAction.ENTER.value:
                ...

        self.cursor_action = CursorAction.NONE.value

    def _process_move_direction(self, buffer):
        if not self.insert_markers: return
        if self.move_direction == MoveDirection.NONE.value: return

        direction = self.move_direction
        for mark in self.insert_markers:
            itr = buffer.get_iter_at_mark(mark)

            if direction == MoveDirection.UP.value:
                new_line = itr.get_line() - 1
                new_itr  = buffer.get_iter_at_line_offset(
                    new_line,
                    itr.get_line_index()
                )

            elif direction == MoveDirection.DOWN.value:
                new_line = itr.get_line() + 1
                new_itr  = buffer.get_iter_at_line_offset(
                    new_line,
                    itr.get_line_index()
                )
            elif direction == MoveDirection.LEFT.value:
                if not itr.backward_char(): break
                new_itr = itr
            elif direction == MoveDirection.RIGHT.value:
                if not itr.forward_char(): break
                new_itr = itr
            else:
                continue

            buffer.move_mark_by_name(mark.get_name(), new_itr)

        self.move_direction = MoveDirection.NONE
