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
        self.was_deleted: bool    = False
        self.buffer: SourceBuffer = SourceBuffer()

        self._set_signals()


    def _set_signals(self):
        self.buffer.set_signals(
            self._changed,
            self._after_changed,
            self._mark_set,
            self._insert_text,
            self._after_insert_text,
            self._modified_changed,
            self._delete_range
        )

    def _changed(self, buffer: SourceBuffer):
        ...

    def _after_changed(self, buffer: SourceBuffer):
        event = Event_Factory.create_event(
            "text_changed",
            file   = self,
            buffer = buffer
        )
        self.emit(event)

    def _insert_text(
        self,
        buffer: SourceBuffer,
        location: Gtk.TextIter,
        text: str, length: int
    ):
        event = Event_Factory.create_event(
            "text_insert",
            file     = self,
            buffer   = self.buffer,
            location = location,
            text     = text,
            length   = length
        )

        # Note: 'idle_add' needed b/c markers don't get thir positions
        #      updated relative to the initial insert.
        #      If not used, seg faults galor during multi insert.
        # GLib.idle_add(self.emit, event)
        self.emit(event)

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
        #      updated relative to the initial insert.
        #      If not used, seg faults galor during multi insert.
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
            file = self,
            buffer = buffer
        )

        self.emit(event)

    def _delete_range(self, buffer: SourceBuffer, start: Gtk.TextIter, end: Gtk.TextIter):
        event = Event_Factory.create_event(
            "delete_range",
            file   = self,
            buffer = buffer,
            start  = start,
            end    = end,
        )

        self.emit(event)

    def _write_file(self, gfile: Gio.File):
        if not gfile: return

        with open(gfile.get_path(), 'w') as f:
            start_itr, end_itr = self.buffer.get_bounds()
            text = self.buffer.get_text(start_itr, end_itr, True)

            f.write(text)

        if self.was_deleted:
            self.was_deleted = False
            self.set_location( None )
            self.set_location( gfile )

        return gfile

    def _load_data(self, text: str, is_new: bool = True):
        undo_manager = self.buffer.get_undo_manager()

        self.buffer.block_changed_signal()
        self.buffer.block_changed_after_signal()
        self.buffer.block_modified_changed_signal()

        def move_insert_to_start():
            start_itr = self.buffer.get_start_iter()
            self.buffer.place_cursor(start_itr)
        undo_manager.begin_not_undoable_action()

        with self.buffer.freeze_notify(): 
            start_itr, end_itr = self.buffer.get_bounds()

            self.buffer.delete(start_itr, end_itr)
            self.buffer.insert(start_itr, text, -1)
            self.is_externally_modified()
            GLib.idle_add(move_insert_to_start)

        undo_manager.end_not_undoable_action()
        self.buffer.set_modified(False)

        if is_new:
            eve = Event_Factory.create_event(
                "loaded_new_file",
                file = self
            )
            self.emit(eve)

        self.buffer.unblock_changed_signal()
        self.buffer.unblock_changed_after_signal()
        self.buffer.unblock_modified_changed_signal()

    def is_externally_modified(self) -> bool:
        if self.fname == "buffer": return

        stat        = os.stat(self.fpath)
        current     = (stat.st_mtime_ns, stat.st_size)
        is_modified = \
            hasattr(self, "last_state") and not current == self.last_state

        self.last_state = current
        return is_modified

    def load_path(self, gfile: Gio.File):
        if not gfile: return
        loaded, contents, etag_out = gfile.load_contents()
        if not loaded: raise Exception("File couldn't be loaded...'")

        # Note:
        # "strict" (default) -> raises an error on invalid bytes
        # "ignore"           -> skips invalid bytes entirely
        # "replace"          -> replaces invalid bytes with �
        # "backslashreplace" -> uses escape sequences like \xFF
        text         = contents.decode("UTF-8", errors = "replace")
        info         = gfile.query_info('standard::content-type', Gio.FileQueryInfoFlags.NONE, None)
        content_type = info.get_content_type()
        self.ftype   = Gio.content_type_get_mime_type(content_type) \
                        .replace("application/", "") \
                        .replace("text/", "") \
                        .replace("x-", "")

        del contents
        self.set_path(gfile)
        logger.debug(f"File content type: {self.ftype}")
        self._load_data(text)

    def set_path(self, gfile: Gio.File):
        if not gfile: return
        self.set_location(gfile)

        self.fpath   = gfile.get_path()
        self.fname   = gfile.get_basename()

        event = Event_Factory.create_event("file_path_set", file = self)
        self.emit(event)

    def reload(self):
        loaded, contents, etag_out = self.get_location().load_contents()
        if not loaded: raise Exception("File couldn't be re-loaded...'")

        text = contents.decode("UTF-8")
        self._load_data(text, False)

    def save(self):
        self._write_file( self.get_location() )

        self.is_externally_modified()
        self.buffer.set_modified(False)
        event = Event_Factory.create_event(
            "saved_file",
            file = self, buffer = self.buffer
        )

        self.emit(event)

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
