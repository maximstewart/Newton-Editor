# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from libs.dto.states import SourceViewStates



class SourceViewsCommandState:
    def __init__(self):
        super(SourceViewsCommandState, self).__init__()


    def focus_in_event(self, source_view, eve, emit):
        return True

    def move_cursor(self, source_view, step, count, extend_selection, emit):
        return True

    def insert_text(self, file, text):
        return True

    def button_press_event(self, source_view, eve):
        return True

    def button_release_event(self, source_view, eve):
        return True

    def key_press_event(self, source_view, eve, key_mapper):
        return True

    def key_release_event(self, source_view, eve, key_mapper):
        return True
