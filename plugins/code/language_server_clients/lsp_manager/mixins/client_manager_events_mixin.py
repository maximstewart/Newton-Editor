# Python imports

# Lib imports

# Application imports
from libs.event_factory import Code_Event_Types



class ClientManagerEventsMixin:
    def _get_controller(self, lang_id, action: str):
        controller = self.clients.get(lang_id)
        if not controller:
            logger.debug(f"No LSP client for '{lang_id}', skipping {action}...")

        return controller

    def _uri(self, fpath: str) -> str:
        return fpath if fpath.startswith("file://") else f"file://{fpath}"

    def _text(self, buffer, *, hidden = False):
        return buffer.get_text(
            *buffer.get_bounds(),
            include_hidden_chars=hidden
        )

    def _version(self, controller, uri, bump = False):
        if bump:
            controller.doc_vers[uri] = controller.doc_vers.get(uri, -1) + 1

        return controller.doc_vers.get(uri, 0)

    def _activate(self, lang_id):
        self.active_language_id = lang_id

    def process_file_load(self, event: Code_Event_Types.AddedNewFileEvent):
        f = event.file
        if not (c := self._get_controller(f.ftype, "didOpen")): return

        uri = self._uri(f.fpath)
        self._activate(f.ftype)

        c._lsp_did_open({
            "uri": uri,
            "language_id": f.ftype,
            "text": self._text(f.buffer),
        })

    def process_file_close(self, event: Code_Event_Types.RemovedFileEvent):
        f = event.file
        if not (c := self._get_controller(f.ftype, "didClose")): return

        uri = self._uri(f.fpath)
        c.doc_vers.pop(uri, None)
        c._lsp_did_close({"uri": uri})

    def process_file_save(self, event: Code_Event_Types.SavedFileEvent):
        f = event.file
        if not (c := self._get_controller(f.ftype, "didSave")): return

        uri = self._uri(f.fpath)
        self._activate(f.ftype)

        c._lsp_did_save({
            "uri": uri,
            "text": self._text(f.buffer),
        })

    def process_file_change(self, event: Code_Event_Types.TextChangedEvent):
        f = event.file
        if not (c := self._get_controller(f.ftype, "didChange")): return

        uri = self._uri(f.fpath)
        self._activate(f.ftype)

        version = self._version(c, uri, bump = True)

        c._lsp_did_change({
            "uri": uri,
            "language_id": f.ftype,
            "version": version,
            "text": self._text(f.buffer, hidden = True),
        })

        it = f.buffer.get_iter_at_mark(f.buffer.get_insert())
        self._set_cache_refresh_trigger(
            f.ftype, f.fpath,
            it.get_line(),
            it.get_line_offset() + 1
        )

    def _iter_pos(self, it):
        return it.get_line(), it.get_line_offset()

    def process_file_text_inserted(self, event: Code_Event_Types.TextInsertedEvent):
        f = event.file
        if not (c := self._get_controller(f.ftype, "didChange")): return

        uri = self._uri(f.fpath)
        self._activate(f.ftype)

        start_it = event.location.copy()
        end_it   = event.location.copy()

        if event.length > 1:
            start_it.backward_chars(event.length)

        sl, sc = self._iter_pos(start_it)
        el, ec = self._iter_pos(end_it)
        sc -= 0 if event.length > 1 else 1
        ec -= 1

        version = self._version(c, uri, bump = True)

        c._lsp_did_change_range({
            "uri": uri,
            "language_id": f.ftype,
            "version": version,
            "text": event.text,
            "line": sl,
            "column": sc,
            "end_line": el,
            "end_column": ec,
        })

        it = event.buffer.get_iter_at_mark(event.buffer.get_insert())
        self._set_cache_refresh_trigger(
            f.ftype, f.fpath, *self._iter_pos(it)
        )

    def process_file_delete_range(self, event: Code_Event_Types.DeleteRangeEvent):
        f = event.file
        if not (c := self._get_controller(f.ftype, "didChange")): return

        uri = self._uri(f.fpath)
        self._activate(f.ftype)

        start_it, end_it = event.start.copy(), event.end.copy()
        if start_it.compare(end_it) > 0:
            start_it, end_it = end_it, start_it

        sl, sc = self._iter_pos(start_it)
        el, ec = self._iter_pos(end_it)

        version = self._version(c, uri, bump = True)

        c._lsp_did_change_range({
            "uri": uri,
            "language_id": f.ftype,
            "version": version,
            "text": "",
            "line": sl,
            "column": sc,
            "end_line": el,
            "end_column": ec,
        })

        it = event.buffer.get_iter_at_mark(event.buffer.get_insert())
        self._set_cache_refresh_trigger(
            f.ftype, f.fpath, *self._iter_pos(it)
        )

    def _request(self, method, lang_id, fpath, **extra):
        if not (c := self._get_controller(lang_id, method)): return

        uri = self._uri(fpath)
        self._activate(lang_id)

        payload = {
            "uri": uri,
            "language_id": lang_id,
            "version": self._version(c, uri),
            **extra
        }

        getattr(c, method)(payload)

    def process_definition(self, lang_id, fpath, line, column):
        self._request("_lsp_definition", lang_id, fpath, line = line, column = column)

    def process_implementation_definition(self, lang_id, fpath, line, column):
        self._request("_lsp_implementation", lang_id, fpath, line = line, column = column)

    def process_references_definition(self, lang_id, fpath, line, column):
        self._request("_lsp_references", lang_id, fpath, line = line, column = column)

    def process_completion_request(self, lang_id, fpath, line, column):
        self._request("_lsp_completion", lang_id, fpath, line = line, column = column)

    def _set_cache_refresh_trigger(self, lang_id, fpath, line, column):
        self.process_completion_request(lang_id, fpath, line, column)
