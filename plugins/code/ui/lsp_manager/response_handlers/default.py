# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from .base import BaseHandler



class DefaultHandler(BaseHandler):
    """Fallback handler for unknown languages - uses generic LSP handling."""

    def handle(self, method: str, response, controller):
        match method:
            case "textDocument/completion":
                self._handle_completion(response)
            case "textDocument/definition":
                self._handle_definition(response, controller)
            case "textDocument/publishDiagnostics":
                self._handle_diagnostics(response)

    def _handle_completion(self, result):
        if not result: return

        items = result.get("items", []) if isinstance(result, dict) else result

        self.response_cache.matchers.clear()
        for item in items:
            label = item.get("label")
            if not label:
                continue

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

            self.response_cache.matchers[label] = {
                "label": label,
                "text": text,
                "info": info,
            }

        self.context._prompt_completion_request()

    def _handle_definition(self, response, controller):
        if not response: return

        uri = response[0]["uri"]
        self.context._prompt_goto_request(uri, response[0]["range"])

    def _handle_diagnostics(self, params):
        if not params: return

        uri = params.get("uri", "")
        diagnostics = params.get("diagnostics", [])

        errors   = []
        warnings = []
        hints    = []

        for diag in diagnostics:
            severity  = diag.get("severity", 1)
            message   = diag.get("message", "")
            range     = diag.get("range", {})

            diag_info = {
                "message": message,
                "range": range
            }

            if severity == 1:
                errors.append(diag_info)
            elif severity == 2:
                warnings.append(diag_info)
            elif severity == 3:
                hints.append(diag_info)

        self.response_cache.lsp_diagnostics = {
            "uri":      uri,
            "errors":   errors,
            "warnings": warnings,
            "hints":    hints
        }

        logger.debug(f"LSP Diagnostics for {uri}: {len(errors)} errors, {len(warnings)} warnings, {len(hints)} hints")
