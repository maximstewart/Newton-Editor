# Python imports

# Lib imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Application imports
from libs.event_factory import Event_Factory
from libs.dto.states import CursorAction

from ..marker_manager import MarkerManager

from .source_view_base_state import SourceViewsBaseState



class SourceViewsMultiInsertState(SourceViewsBaseState):
    def __init__(self):
        super(SourceViewsMultiInsertState, self).__init__()

        self.cursor_action: CursorAction   = None
        self.marker_manager: MarkerManager = MarkerManager()


    def insert_text(self, file, text: str) -> bool:
        if not self.marker_manager.buffer_markers: return False

        buffer = file.buffer

        if buffer.is_processing_completion:
            return self._insert_completion_text(buffer, text)

        def insert_text(start_itr, end_itr = None):
            if not end_itr:
                buffer.insert(start_itr, text, -1)
                return

            buffer.delete(start_itr, end_itr)
            buffer.insert(start_itr, text, -1)

        self.marker_manager.apply_to_marks(buffer, insert_text)
        return True

    def _insert_completion_text(self, buffer, text: str) -> bool:
        buffer.is_processing_completion = False

        def replace_word(start_itr, end_itr = None):
            if not end_itr:
                end_itr = start_itr.copy()

            if not start_itr.starts_word():
                start_itr.backward_word_start()

            if not end_itr.ends_word():
                end_itr.forward_word_end()

            buffer.delete(start_itr, end_itr)
            buffer.insert(start_itr, text, -1)

        self.marker_manager.apply_to_marks(buffer, replace_word)

        return True

    def move_cursor(
        self, source_view, step, count, is_selection,
        emit = None, ignore_leader: bool = False
    ):
        is_forward    = count > 0
        buffer        = source_view.get_buffer()

        start_mark    = buffer.get_insert()
        end_mark      = buffer.get_selection_bound()
        start_itr     = buffer.get_iter_at_mark(start_mark)
        end_itr       = buffer.get_iter_at_mark(end_mark)
        has_selection = not start_itr.equal(end_itr)

        step_map      = {
            Gtk.MovementStep.LOGICAL_POSITIONS: ("char", self.marker_manager.move_by_char),
            Gtk.MovementStep.VISUAL_POSITIONS:  ("char", self.marker_manager.move_by_char),
            Gtk.MovementStep.WORDS:             ("word", self.marker_manager.move_by_word),
            Gtk.MovementStep.DISPLAY_LINES:     ("line", self.marker_manager.move_by_line),
        }

        kind, move_fn = step_map[step]
        move_fn(buffer, is_forward, is_selection)

        if ignore_leader: return True

        self.marker_manager._proc_move(
            buffer,
            is_forward,
            is_selection,
            kind,
            None,
            start_mark,
            end_mark,
            has_selection,
            start_itr,
            end_itr,
        )

        # self._signal_cursor_moved(source_view, emit)

        return True

    def key_press_event(self, source_view, event, key_mapper):
        char = key_mapper.get_raw_keyname(event).upper()
        self.is_control = key_mapper.is_control(event)
        self.is_shift   = key_mapper.is_shift(event)
        self.is_super   = key_mapper.is_super(event)

        if char.upper() in ["BACKSPACE", "DELETE", "ENTER"]:
            self.marker_manager.process_cursor_action(
                source_view.get_buffer(),
                char.upper()
            )
            return False

        if self._do_cursor_moved(source_view, char):
            return True

        return super().key_press_event(source_view, event, key_mapper)

    def button_press_event(self, source_view, event):
        return True

    def button_release_event(self, source_view, event):
        self.marker_manager.button_release_event(source_view, event)

    def _do_cursor_moved(self, source_view, char: str):
        key = char.upper()
        if key not in {"LEFT", "RIGHT", "UP", "DOWN"}: return False

        direction = {
            "LEFT":  -1,
            "RIGHT":  1,
            "UP":    -1,
            "DOWN":   1,
        }[key]

        is_horizontal = key in {"LEFT", "RIGHT"}

        step  = \
            Gtk.MovementStep.VISUAL_POSITIONS if is_horizontal else Gtk.MovementStep.DISPLAY_LINES
        count = direction
        is_selection = self.is_shift

        if is_horizontal:
            if self.is_control:
                step = Gtk.MovementStep.WORDS
            if self.is_control and self.is_shift:
                is_selection = True
            if self.is_super:
                return self.move_cursor(
                    source_view,
                    step,
                    count,
                    is_selection  = False,
                    emit          = None,
                    ignore_leader = True,
                )
        else:
            if self.is_super:
                return self.move_cursor(
                    source_view,
                    step,
                    count,
                    is_selection,
                    emit          = None,
                    ignore_leader = True,
                )

        return self.move_cursor(
            source_view,
            step         = step,
            count        = count,
            is_selection = is_selection,
        )

    def _signal_cursor_moved(self, source_view, emit):
        buffer = source_view.get_buffer()
        itr    = buffer.get_iter_at_mark( buffer.get_insert() )
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

