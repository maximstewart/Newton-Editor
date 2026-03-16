# Python imports

# Lib imports
import gi

from gi.repository import GLib

# Application imports
from libs.event_factory import Code_Event_Types



class LSPClientEventsMixin:

    def process_file_load(self, event: Code_Event_Types.AddedNewFileEvent):
        lang_id = event.file.ftype
        if lang_id not in self.clients:
            logger.debug(f"No LSP client for '{lang_id}', skipping didOpen")
            return

        controller = self.clients[lang_id]
        fpath      = event.file.fpath
        uri        = f"file://{fpath}" if not fpath.startswith("file://") else fpath
        buffer     = event.file.buffer
        text       = buffer.get_text(*buffer.get_bounds())
        self.active_language_id = lang_id

        controller._lsp_did_open({
            "uri": uri,
            "language_id": lang_id,
            "text": text
        })

    def process_file_close(self, event: Code_Event_Types.RemovedFileEvent):
        lang_id = event.file.ftype
        if lang_id not in self.clients:
            logger.debug(f"No LSP client for '{lang_id}', skipping didClose")
            return

        controller = self.clients[lang_id]
        fpath      = event.file.fpath
        uri        = f"file://{fpath}" if not fpath.startswith("file://") else fpath

        controller._lsp_did_close({"uri": uri})

    def process_file_save(self, event: Code_Event_Types.SavedFileEvent):
        lang_id = event.file.ftype
        if lang_id not in self.clients:
            logger.debug(f"No LSP client for '{lang_id}', skipping didSave")
            return

        controller = self.clients[lang_id]
        fpath      = event.file.fpath
        uri        = f"file://{fpath}" if not fpath.startswith("file://") else fpath
        buffer     = event.file.buffer
        text       = buffer.get_text(*buffer.get_bounds())
        self.active_language_id = lang_id

        controller._lsp_did_save({"uri": uri, "text": text})

    def process_file_change(self, event: Code_Event_Types.TextChangedEvent):
        self._clear_delayed_cache_refresh_trigger()

        lang_id = event.file.ftype
        if lang_id not in self.clients:
            logger.debug(f"No LSP client for '{lang_id}', skipping didChange")
            return

        controller = self.clients[lang_id]
        fpath      = event.file.fpath
        uri        = f"file://{fpath}" if not fpath.startswith("file://") else fpath
        buffer     = event.file.buffer
        text       = buffer.get_text(*buffer.get_bounds())
        self.active_language_id = lang_id

        controller._lsp_did_change({
            "uri": uri,
            "language_id": lang_id,
            "version": 1,
            "text": text
        })

        iter   = buffer.get_iter_at_mark( buffer.get_insert() )
        line   = iter.get_line()
        column = iter.get_line_offset()
        self._set_cache_refresh_trigger(
            lang_id, fpath, line, column
        )


    def process_goto_definition(
        self, lang_id: str, fpath: str, line: int, column: int
    ):
        if lang_id not in self.clients:
            logger.debug(f"No LSP client for '{lang_id}', skipping goto definition")
            return

        controller = self.clients[lang_id]
        uri        = f"file://{fpath}" if not fpath.startswith("file://") else fpath
        self.active_language_id = lang_id

        controller._lsp_definition({
            "uri": uri,
            "language_id": lang_id,
            "version": 1,
            "line": line,
            "column": column
        })

    def process_completion_request(
        self, lang_id: str, fpath: str, line: int, column: int
    ):
        if lang_id not in self.clients:
            logger.debug(f"No LSP client for '{lang_id}', skipping completion")
            return

        controller = self.clients[lang_id]
        uri        = f"file://{fpath}" if not fpath.startswith("file://") else fpath
        self.active_language_id = lang_id

        controller._lsp_completion({
            "uri": uri,
            "language_id": lang_id,
            "version": 1,
            "line": line,
            "column": column
        })


    def _clear_delayed_cache_refresh_trigger(self):
        if self._cache_refresh_timeout_id:
            GLib.source_remove(self._cache_refresh_timeout_id)

    def _set_cache_refresh_trigger(
        self, lang_id: str, fpath: str, line: int, column: int
    ):
        def trigger_cache_refresh(lang_id, fpath, line, column):
            self._cache_refresh_timeout_id = None
            self.process_completion_request(
                lang_id, fpath, line, column
            )
            return False

        self._cache_refresh_timeout_id = GLib.timeout_add(1500, trigger_cache_refresh, lang_id, fpath, line, column)
