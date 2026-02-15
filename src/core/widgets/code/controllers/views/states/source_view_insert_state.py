# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from libs.dto.states import SourceViewStates



class SourceViewsInsertState:
    def __init__(self):
        super(SourceViewsInsertState, self).__init__()


    def focus_in_event(self, source_view, eve, emit):
        source_view.command.exec("set_miniview")
        source_view.command.exec("set_focus_border")
        source_view.command.exec("update_info_bar")

        event = Event_Factory.create_event("focused_view", view = source_view)
        emit(event)

    def insert_text(self, file, text):
        return True

    def move_cursor(self, source_view, step, count, extend_selection, emit):
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

        source_view.command.exec("update_info_bar")

    def button_press_event(self, source_view, eve):
        source_view.command.exec("update_info_bar")

    def button_release_event(self, source_view, eve):
        source_view.command.exec("update_info_bar")

    def key_press_event(self, source_view, eve, key_mapper):
        command   = key_mapper._key_press_event(eve)
        is_future = key_mapper._key_release_event(eve)

        if is_future: return True
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
