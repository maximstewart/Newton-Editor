# Python imports
import os

# Lib imports
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GtkSource
from gi.repository import Gio

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from .source_buffer import SourceBuffer



class SourceFile(GtkSource.File):
    def __init__(self):
        super(SourceFile, self).__init__()

        self.encoding: str        = "UTF-8"
        self.fname: str           = "buffer"
        self.fpath: str           = "buffer"
        self.ftype: str           = "buffer"

        self.buffer: SourceBuffer = SourceBuffer()

        self._set_signals()


    def _set_signals(self):
        self.buffer.set_signals(
            self._changed,
            self._mark_set,
            self._insert_text,
            self._after_insert_text,
            self._modified_changed
        )

    def _changed(self, buffer: SourceBuffer):
        event = Event_Factory.create_event("text_changed", buffer = buffer)
        event.file = self
        self.emit(event)

    def _insert_text(
        self,
        buffer: SourceBuffer,
        location: Gtk.TextIter,
        text: str, length: int
    ):
        ...

    def _after_insert_text(
        self,
        buffer: SourceBuffer,
        location: Gtk.TextIter,
        text: str, length: int
    ):
        event = Event_Factory.create_event(
            "text_inserted",
            file     = self,
            buffer   = self.buffer,
            location = location,
            text     = text,
            length   = length
        )

        # Note: 'idle_add' needed b/c markers don't get thir positions
        #       updated relative to the initial insert.
        #       If not used, seg faults galor during multi insert.
        GLib.idle_add(self.emit, event)

    def _mark_set(
        self,
        buffer: SourceBuffer,
        location: Gtk.TextIter,
        mark: Gtk.TextMark
    ):
        # event = Event_Factory.create_event(
        #     "mark_set",
        #     file = self, buffer = buffer
        # )

        # self.emit(event)
        ...

    def _modified_changed(self, buffer: SourceBuffer):
        event = Event_Factory.create_event(
            "modified_changed",
            file = self, buffer = buffer
        )

        self.emit(event)

    def _write_file(self, gfile: Gio.File):
        if not gfile: return

        with open(gfile.get_path(), 'w') as f:
            start_itr, end_itr = self.buffer.get_bounds()
            text = self.buffer.get_text(start_itr, end_itr, True)

            f.write(text)

        return gfile


    def load_path(self, gfile: Gio.File):
        if not gfile: return

        self.set_path(gfile)
        data         = gfile.load_bytes()[0].get_data().decode("UTF-8")
        undo_manager = self.buffer.get_undo_manager()

        undo_manager.begin_not_undoable_action()
        self.buffer.insert_at_cursor(data)
        undo_manager.end_not_undoable_action()

    def set_path(self, gfile: Gio.File):
        if not gfile: return
        self.set_location(gfile)

        self.fpath   = gfile.get_path()
        self.fname   = gfile.get_basename()

        event = Event_Factory.create_event("file_path_set", file = self)
        self.emit(event)

    def save(self):
        event = Event_Factory.create_event(
            "saved_file",
            file = self, buffer = self.buffer
        )

        self.emit(event)
        self._write_file( self.get_location() )

    def save_as(self):
        file = event_system.emit_and_await("save-file-dialog")
        if not file: return

        self._write_file(file)
        self.set_path(file)

        return file

    def close(self):
        del self.buffer

    def emit(self, event: Code_Event_Types.CodeEvent):
        ...

    def emit_to(self, controller: str, event: Code_Event_Types.CodeEvent):
        ...
