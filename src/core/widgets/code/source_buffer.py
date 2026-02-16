# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')
from gi.repository import GtkSource

# Application imports



class SourceBuffer(GtkSource.Buffer):
    def __init__(self):
        super(SourceBuffer, self).__init__()

        self.is_processing_completion: bool = False

        self._handler_ids = []


    def set_signals(
        self,
        _changed,
        _mark_set,
        _insert_text,
        _after_insert_text,
        _modified_changed,
    ):

        self._handler_ids = [
            self.connect("changed",           _changed),
            self.connect("mark-set",          _mark_set),
            self.connect("insert-text",       _insert_text),
            self.connect_after("insert-text", _after_insert_text),
            self.connect("modified-changed",  _modified_changed)
        ]

    def block_changed_signal(self):
        self.handler_block(self._handler_ids[0])

    def block_insert_after_signal(self):
        self.handler_block(self._handler_ids[3])

    def block_modified_changed_signal(self):
        self.handler_block(self._handler_ids[4])

    def unblock_changed_signal(self):
        self.handler_unblock(self._handler_ids[0])

    def unblock_insert_after_signal(self):
        self.handler_unblock(self._handler_ids[3])

    def unblock_modified_changed_signal(self):
        self.handler_unblock(self._handler_ids[4])

    def clear_signals(self):
        for handle_id in self._handler_ids:
            self.disconnect(handle_id)

    def __del__(self):
        for handle_id in self._handler_ids:
            self.disconnect(handle_id)

