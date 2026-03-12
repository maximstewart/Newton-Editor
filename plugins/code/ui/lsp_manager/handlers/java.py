# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from .default import DefaultHandler



class JavaHandler(DefaultHandler):
    """Java-specific: overrides definition, handles classFileContents."""

    def handle(self, method: str, response, controller):
        match method:
            case "textDocument/definition":
                self._handle_definition(response, controller)
            case "java/classFileContents":
                self._handle_class_file_contents(response)
            case _:
                super().handle(method, response, controller)

    def _handle_definition(self, response, controller):
        if not response: return

        uri = response[0]["uri"]
        if "jdt://" in uri:
            controller._lsp_java_class_file_contents(uri)
            return

        self.context._prompt_goto_request(uri, response[0]["range"])

    def _handle_class_file_contents(self, text: str):
        event = Event_Factory.create_event("get_active_view")
        self.context.emit_to("source_views", event)

        view = event.response
        file = view.command.exec("new_file")
        buffer = view.get_buffer()
        itr = buffer.get_iter_at_mark(buffer.get_insert())
        lm = GtkSource.LanguageManager.get_default()
        language = lm.get_language("java")
        file.ftype = "java"

        buffer.set_language(language)
        buffer.insert(itr, text, -1)
