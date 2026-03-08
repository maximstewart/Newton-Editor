# Python imports

# Lib imports
import gi

from gi.repository import GLib

# Application imports
from libs.event_factory import Code_Event_Types



class LSPServerEventsMixin:

    def _handle_definition_response(self, result: dict or list):
        if not result: return
        self._prompt_goto_request(result[0]["uri"])

    def _handle_completion_response(self, result: dict or list):
        if not result: return

        items = []
        if isinstance(result, dict):
            items = result.get("items", [])
        elif isinstance(result, list):
            items = result

        self.matchers.clear()
        for item in items:
            label = item.get("label", "")
            if not label: continue

            text = item.get("insertText")
            if not text and "textEdit" in item:
                text = item["textEdit"].get("newText", "")

            info = ""
            if "detail" in item:
                info = item["detail"]
            elif "documentation" in item:
                doc = item["documentation"]
                if isinstance(doc, dict):
                    info = doc.get("value", "")
                else:
                    info = str(doc)

            self.matchers[label] = {
                "label": label,
                "text": text,
                "info": info
            }

        self._prompt_completion_request()

    def _prompt_completion_request(self):
        raise NotImplementedError

    def _prompt_goto_request(self, uri: str):
        raise NotImplementedError
