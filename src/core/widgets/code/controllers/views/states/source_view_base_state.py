# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from libs.dto.states import SourceViewStates



class SourceViewsBaseState:
    def __init__(self):
        super(SourceViewsBaseState, self).__init__()


    def focus_in_event(self, source_view, eve, emit):
        source_view.command.exec("set_miniview")
        source_view.command.exec("set_focus_border")
        source_view.command.exec("update_info_bar")

        event = Event_Factory.create_event("focused_view", view = source_view)
        emit(event)

    def insert_text(self, file, text: str):

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
        ...

    def button_release_event(self, source_view, eve):
        source_view.command.exec("update_info_bar")

    def key_press_event(self, source_view, eve, key_mapper):
        command        = key_mapper._key_press_event(eve)
        is_future      = key_mapper._key_release_event(eve)
        char_str       = key_mapper.get_char(eve)
        modkeys_states = key_mapper.get_modkeys_states(eve)

        if is_future:   return True
        if not command: return False

        response = source_view.command.exec_with_args(
            command, source_view, char_str, modkeys_states
        )

        return True if not response else response

    def key_release_event(self, source_view, eve, key_mapper):
        command        = key_mapper._key_release_event(eve)
        is_past        = key_mapper._key_press_event(eve)
        char_str       = key_mapper.get_char(eve)
        modkeys_states = key_mapper.get_modkeys_states(eve)

        if is_past: return True
        if not command: return False

        response = source_view.command.exec_with_args(
            command, source_view, char_str, modkeys_states
        )

        return True if not response else response

    def populate_popup(self, source_view, menu, emit):
        buffer = source_view.get_buffer()
        event  = Event_Factory.create_event(
            "populate_source_view_popup",
            buffer = buffer,
            menu   = menu
        )

        emit(event)

        menu.show_all()
