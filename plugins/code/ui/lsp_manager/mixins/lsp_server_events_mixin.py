# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GLib
from gi.repository import GtkSource

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types



class LSPServerEventsMixin:

    def _handle_definition_response(self, uri: str, pointer_pos: dict):
        self._prompt_goto_request(uri, pointer_pos)

    def _handle_completion_response(self, result: dict or list):
        if not result: return

        items = []
        if isinstance(result, dict):
            items = result.get("items", [])
        elif isinstance(result, list):
            items = result

        self.matchers.clear()
        for item in items:
            label = item.get("label")
            if not label: return None

            text = (
                item.get("insertText")
                or item.get("textEdit", {}).get("newText")
                or item.get("textEditText", "")
                or label
            )

            detail = item.get("detail")
            doc    = item.get("documentation")

            if detail:
                info = detail
            elif isinstance(doc, dict):
                info = doc.get("value", "")
            else:
                info = str(doc) if doc else ""

            self.matchers[label] = {
                "label": label,
                "text": text,
                "info": info
            }

        self._prompt_completion_request()


    def _prompt_goto_request(self, uri: str, pointer_pos: dict):
        event  = Event_Factory.create_event(
            "get_active_view",
        )
        self.emit_to("source_views", event)
        view = event.response
        view._on_uri_data_received( [uri] )

        buffer = view.get_buffer()

        def move_cursor(buffer, pointer_pos):
            itr = buffer.get_iter_at_line( pointer_pos["end"]["line"] )
            itr.forward_chars( pointer_pos["end"]["character"] )
            buffer.place_cursor(itr)
            view.scroll_to_iter(itr, 0.2, False, 0, 0)

        GLib.idle_add( move_cursor, buffer, pointer_pos )

    def _handle_java_class_file_contents(self, text: str):
        event  = Event_Factory.create_event(
            "get_active_view",
        )
        self.emit_to("source_views", event)

        view       = event.response
        file       = view.command.exec("new_file")
        buffer     = view.get_buffer()
        itr        = buffer.get_iter_at_mark( buffer.get_insert() )
        lm         = GtkSource.LanguageManager.get_default()
        language   = lm.get_language("java")
        file.ftype = "java"

        buffer.set_language(language)
        buffer.insert(itr, text, -1)
