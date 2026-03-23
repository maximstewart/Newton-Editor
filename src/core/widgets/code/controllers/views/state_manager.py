# Python imports

# Lib imports

# Application imports
from libs.dto.states import SourceViewStates

from ...key_mapper import KeyMapper

from .states import *



class SourceViewStateManager:
    def __init__(self):
        self.key_mapper: KeyMapper = KeyMapper()
        
        self.states: dict = {
            SourceViewStates.INSERT:      SourceViewsInsertState(),
            SourceViewStates.MULTIINSERT: SourceViewsMultiInsertState(),
            SourceViewStates.COMMAND:     SourceViewsCommandState(),
            SourceViewStates.READONLY:    SourceViewsReadOnlyState(),
            SourceViewStates.INDEPENDENT: SourceViewsIndependentState()
        }


    def handle_focus_in_event(self, source_view, eve, emit):
        return self.states[source_view.state].focus_in_event(source_view, eve, emit)

    def handle_insert_text(self, source_view, file, text):
        return self.states[source_view.state].insert_text(file, text)

    def handle_move_cursor(self, source_view, step, count, extend_selection, emit):
        return self.states[source_view.state].move_cursor(
            source_view, step, count, extend_selection, emit
        )

    def handle_key_press_event(self, source_view, eve):
        return self.states[source_view.state].key_press_event(
            source_view, eve, self.key_mapper
        )

    def handle_key_release_event(self, source_view, eve):
        return self.states[source_view.state].key_release_event(
            source_view, eve, self.key_mapper
        )

    def handle_button_press_event(self, source_view, eve):
        self._handle_multi_insert_toggle(source_view, eve)

        return self.states[source_view.state].button_press_event(source_view, eve)

    def handle_button_release_event(self, source_view, eve):
        return self.states[source_view.state].button_release_event(source_view, eve)

    def handle_scroll_event(self, source_view, eve):
        return self.states[source_view.state].scroll_event(
            source_view, eve, self.key_mapper
        )

    def handle_populate_popup(self, source_view, menu, emit):
        return self.states[source_view.state].populate_popup(
            source_view, menu, emit
        )

    def _handle_multi_insert_toggle(self, source_view, eve):
        is_control = self.key_mapper.is_control(eve)
        if is_control and not source_view.state == SourceViewStates.MULTIINSERT:
            logger.debug("Entered Multi-Insert Mode...")
            source_view.state = SourceViewStates.MULTIINSERT

        if not is_control and source_view.state == SourceViewStates.MULTIINSERT:
            logger.debug("Entered Regular Insert Mode...")
            self.states[source_view.state].marker_manager.clear_mark_sets(source_view)

            source_view.state = SourceViewStates.INSERT

