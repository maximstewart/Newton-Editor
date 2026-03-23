# Python imports

# Lib imports
import gi

from gi.repository import GLib

# Application imports
from ...source_view import SourceView



class SourceViewSignalMapper:
    def __init__(self):
        self.active_view: SourceView = None


    def bind_emit(self, emit: callable):
        self.emit = emit

    def set_state_manager(self, state_manager):
        self.state_manager = state_manager

    def set_buffer_to_active_view(self, buffer):
        self.active_view.set_buffer(buffer)
        self.active_view.command.exec("update_info_bar")
        GLib.idle_add(self._scroll_to_iter)

    def connect_signals(self, source_view: SourceView):
        signal_mappings = self._get_signal_mappings()
        for signal, handler in signal_mappings.items():
            if not signal == "populate-popup": 
                source_view.connect(signal, handler)
                continue

            source_view.connect_after(signal, handler)

    def disconnect_signals(self, source_view: SourceView):
        signal_mappings = self._get_signal_mappings()
        for signal, handler in signal_mappings.items():
            source_view.disconnect_by_func(handler)

    def insert_text(self, file, string: str):
        return self.state_manager.handle_insert_text(self.active_view, file, string)

    def _scroll_to_iter(self):
        buffer = self.active_view.get_buffer()
        itr    = buffer.get_iter_at_mark( buffer.get_insert() )

        self.active_view.scroll_to_iter(itr, 0.2, False, 0, 0)

    def _get_signal_mappings(self):
        return {
            "focus-in-event":       self._focus_in_event,
            "move-cursor":          self._move_cursor,
            "key-press-event":      self._key_press_event,
            "key-release-event":    self._key_release_event,
            "button-press-event":   self._button_press_event,
            "button-release-event": self._button_release_event,
            "scroll-event":         self._scroll_event,
            "populate-popup":       self._populate_popup
        }

    def _focus_in_event(self, source_view: SourceView, eve):
        self.active_view = source_view
        return self.state_manager.handle_focus_in_event(source_view, eve, self.emit)

    def _move_cursor(self, source_view: SourceView, step, count, extend_selection):
        return self.state_manager.handle_move_cursor(
            source_view, step, count, extend_selection, self.emit
        )

    def _key_press_event(self, source_view: SourceView, eve):
        return self.state_manager.handle_key_press_event(source_view, eve)

    def _key_release_event(self, source_view: SourceView, eve):
        return self.state_manager.handle_key_release_event(source_view, eve)

    def _button_press_event(self, source_view: SourceView, eve):
        return self.state_manager.handle_button_press_event(source_view, eve)

    def _button_release_event(self, source_view: SourceView, eve):
        return self.state_manager.handle_button_release_event(source_view, eve)

    def _scroll_event(self, source_view: SourceView, eve):
        return self.state_manager.handle_scroll_event(source_view, eve)

    def _populate_popup(self, source_view: SourceView, menu):
        return self.state_manager.handle_populate_popup(source_view, menu, self.emit)
