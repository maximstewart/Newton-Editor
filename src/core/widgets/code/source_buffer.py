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
        self.is_processing_completion: bool = False

        self.create_tag(
            "search-highlight",
            background = "yellow",
            foreground = "black"
        )


    def set_signals(
        self,
        _changed,
        _after_changed,
        _mark_set,
        _insert_text,
        _after_insert_text,
        _modified_changed,
        _delete_range,
    ):

        self._handler_ids = [
            self.connect("changed",           _changed),
            self.connect_after("changed",     _after_changed),
            self.connect("mark-set",          _mark_set),
            self.connect("insert-text",       _insert_text),
            self.connect_after("insert-text", _after_insert_text),
            self.connect("modified-changed",  _modified_changed),
            self.connect("delete-range",      _delete_range)
        ]

    def block_changed_signal(self):
        self.handler_block(self._handler_ids[0])

    def block_changed_after_signal(self):
        self.handler_block(self._handler_ids[1])

    def block_insert_after_signal(self):
        self.handler_block(self._handler_ids[4])

    def block_modified_changed_signal(self):
        self.handler_block(self._handler_ids[5])

    def block_delete_range(self):
        self.handler_block(self._handler_ids[6])

    def unblock_changed_signal(self):
        self.handler_unblock(self._handler_ids[0])

    def unblock_changed_after_signal(self):
        self.handler_unblock(self._handler_ids[1])

    def unblock_insert_after_signal(self):
        self.handler_unblock(self._handler_ids[4])

    def unblock_modified_changed_signal(self):
        self.handler_unblock(self._handler_ids[5])

    def unblock_delete_range(self):
        self.handler_block(self._handler_ids[6])

    def clear_signals(self):
        for handle_id in self._handler_ids:
            self.disconnect(handle_id)

    def __del__(self):
        self.clear_signals()
