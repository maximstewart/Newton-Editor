# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types
from libs.dto.states import SourceViewStates, MoveDirection, CursorAction

from ....mixins.source_mark_events_mixin import MarkEventsMixin



class SourceViewsMultiInsertState(MarkEventsMixin):
    def __init__(self):
        super(SourceViewsMultiInsertState, self).__init__()

        self.cursor_action: CursorAction    = 0
        self.move_direction: MoveDirection  = 0
        self.insert_markers: list           = []


    def focus_in_event(self, source_view, eve, emit):
        source_view.command.exec("set_miniview")
        source_view.command.exec("set_focus_border")
        source_view.command.exec("update_info_bar")

        event = Event_Factory.create_event("focused_view", view = source_view)
        emit(event)

    def insert_text(self, file, text):
        if not self.insert_markers: return False

        buffer = file.buffer
        if buffer.is_processing_completion:
            self.insert_completion_text(buffer, text)
            return True

        # freeze buffer and insert to each mark (if any)
        buffer.block_insert_after_signal()
        buffer.begin_user_action()

        with buffer.freeze_notify(): 
            for mark in self.insert_markers:
                itr = buffer.get_iter_at_mark(mark)
                buffer.insert(itr, text, -1)

        buffer.end_user_action()
        buffer.unblock_insert_after_signal()

        return True

    def insert_completion_text(self, buffer, text):
        buffer.is_processing_completion = False

        # freeze buffer and insert to each mark (if any)
        buffer.block_insert_after_signal()
        buffer.begin_user_action()

        with buffer.freeze_notify(): 
            for mark in self.insert_markers:
                end_itr = buffer.get_iter_at_mark(mark)
                start_itr = end_itr.copy()

                if not start_itr.starts_word():
                    start_itr.backward_word_start()

                if not end_itr.ends_word():
                    end_itr.forward_word_end()

                buffer.delete(start_itr, end_itr)
                buffer.insert(start_itr, text, -1)

        buffer.end_user_action()
        buffer.unblock_insert_after_signal()

        return True

    def move_cursor(self, source_view, step, count, extend_selection, emit):
        buffer = source_view.get_buffer()

        self._process_move_direction(buffer)
        self._signal_cursor_moved(source_view, emit)
        source_view.command.exec("update_info_bar")

    def button_press_event(self, source_view, eve):
        source_view.command.exec("update_info_bar")
        return True

    def button_release_event(self, source_view, eve):
        buffer      = source_view.get_buffer()
        insert_iter = buffer.get_iter_at_mark( buffer.get_insert() )
        data        = source_view.window_to_buffer_coords(
            Gtk.TextWindowType.TEXT,
            eve.x,
            eve.y
        )
        is_over_text, \
        target_iter,  \
        is_trailing   = source_view.get_iter_at_position(data.buffer_x, data.buffer_y)

        if not is_over_text:
            # NOTE: Trying to put at very end of line if not over text (aka, clicking right of text)
            target_iter.forward_visible_line()
            target_iter.backward_char()

        self._insert_mark(insert_iter, target_iter, buffer)

    def key_press_event(self, source_view, eve, key_mapper):
        char = key_mapper.get_raw_keyname(eve)

        for action in CursorAction:
            if not action.name == char.upper(): continue
            self.cursor_action = action.value
            self._process_cursor_action(source_view.get_buffer())

            return False

        for direction in MoveDirection:
            if not direction.name == char.upper(): continue
            self.move_direction = direction.value
            return False

        is_future = key_mapper._key_release_event(eve)
        if is_future: return True

        command = key_mapper._key_press_event(eve)
        if not command: return False

        source_view.command.exec(command)

        return True

    def key_release_event(self, source_view, eve, key_mapper):
        command = key_mapper._key_release_event(eve)
        is_past = key_mapper._key_press_event(eve)

        if is_past: return True
        if not command: return False

        source_view.command.exec(command)

        return True

    def _signal_cursor_moved(self, source_view, emit):
        buffer = source_view.get_buffer()
        itr   = buffer.get_iter_at_mark( buffer.get_insert() )
        line   = itr.get_line()
        char   = itr.get_line_offset()
        event  = Event_Factory.create_event(
            "cursor_moved",
            view   = source_view,
            buffer = buffer,
            line   = line,
            char   = char
        )

        emit(event)
