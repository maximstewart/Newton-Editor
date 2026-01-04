# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')
from gi.repository import GtkSource

# Application imports



class SourceBuffer(GtkSource.Buffer):
    def __init__(self):
        super(SourceBuffer, self).__init__()

        self._handler_ids = []


    def set_signals(
        self,
        _changed,
        _mark_set,
        _insert_text,
        _modified_changed,
    ):

        self._handler_ids = [
            self.connect("changed",          _changed),
            self.connect("mark-set",         _mark_set),
            self.connect("insert-text",      _insert_text),
            self.connect("modified-changed", _modified_changed)
        ]

    def clear_signals(self):
        for handle_id in self._handler_ids:
            self.disconnect(handle_id)

    def __del__(self):
        for handle_id in self._handler_ids:
            self.disconnect(handle_id)