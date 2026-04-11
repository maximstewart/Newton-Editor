# Python imports
import os

# Lib imports

# Application imports
from ..dto.code.lsp.lsp_messages import get_message_obj
from ..dto.code.lsp.lsp_messages import didopen_notification
from ..dto.code.lsp.lsp_messages import didsave_notification
from ..dto.code.lsp.lsp_messages import didclose_notification
from ..dto.code.lsp.lsp_messages import didchange_notification
from ..dto.code.lsp.lsp_messages import didchange_notification_range
from ..dto.code.lsp.lsp_messages import completion_request
from ..dto.code.lsp.lsp_messages import definition_request
from ..dto.code.lsp.lsp_messages import implementation_request
from ..dto.code.lsp.lsp_messages import references_request
from ..dto.code.lsp.lsp_messages import symbols_request



class LSPClientEvents:
    def send_initialize_message(self):
        folder_name   = os.path.basename(self._workspace_path)
        workspace_uri = f"file://{self._workspace_path}"

        self._init_params["processId"]        = None
        self._init_params["rootPath"]         = self._workspace_path
        self._init_params["rootUri"]          = workspace_uri
        self._init_params["workspaceFolders"] = [
            {
                "name": folder_name,
                "uri": workspace_uri
            }
        ]

        self._init_params["initializationOptions"] = self._init_opts
        self.send_request("initialize", self._init_params)

    def send_initialized_message(self):
        self.send_notification("initialized")

    def _lsp_did_open(self, data: dict):
        method = "textDocument/didOpen"
        params = didopen_notification["params"]
        self.doc_vers[ data["uri"] ] = -1

        params["textDocument"]["uri"]        = data["uri"]
        params["textDocument"]["languageId"] = data["language_id"]
        params["textDocument"]["text"]       = data["text"]

        self.send_notification( method, params )

    def _lsp_did_save(self, data: dict):
        method = "textDocument/didSave"
        params = didsave_notification["params"]

        params["textDocument"]["uri"] = data["uri"]
        params["text"]                = data["text"]

        self.send_notification( method, params )

    def _lsp_did_close(self, data: dict):
        method = "textDocument/didClose"
        params = didclose_notification["params"]

        params["textDocument"]["uri"] = data["uri"]

        self.send_notification( method, params )

    def _lsp_did_change(self, data: dict):
        method = "textDocument/didChange"
        params = didchange_notification["params"]

        params["textDocument"]["uri"]        = data["uri"]
        params["textDocument"]["languageId"] = data["language_id"]
        params["textDocument"]["version"]    = data["version"]

        contentChanges         = params["contentChanges"][0]
        contentChanges["text"] = data["text"]

        self.send_notification( method, params )

    def _lsp_did_change_range(self, data: dict):
        method = "textDocument/didChange"
        params = didchange_notification_range["params"]

        params["textDocument"]["uri"]        = data["uri"]
        params["textDocument"]["languageId"] = data["language_id"]
        params["textDocument"]["version"]    = data["version"]

        contentChanges         = params["contentChanges"][0]
        start                  = contentChanges["range"]["start"]
        end                    = contentChanges["range"]["end"]
        contentChanges["text"] = data["text"]
        start["line"]          = data["line"]
        start["character"]     = data["column"]
        end["line"]            = data["end_line"]
        end["character"]       = data["end_column"]

        self.send_notification( method, params )

    def _lsp_definition(self, data: dict):
        method = "textDocument/definition"
        params = definition_request["params"]

        params["textDocument"]["uri"]        = data["uri"]
        params["textDocument"]["languageId"] = data["language_id"]
        params["textDocument"]["version"]    = data["version"]
        params["position"]["line"]           = data["line"]
        params["position"]["character"]      = data["column"]

        self.send_request( method, params )

    def _lsp_implementation(self, data: dict):
        method = "textDocument/implementation"
        params = implementation_request["params"]

        params["textDocument"]["uri"]        = data["uri"]
        params["position"]["line"]           = data["line"]
        params["position"]["character"]      = data["column"]

        self.send_request( method, params )

    def _lsp_references(self, data: dict):
        method = "textDocument/references"
        params = references_request["params"]

        params["textDocument"]["uri"]        = data["uri"]
        params["textDocument"]["languageId"] = data["language_id"]
        params["textDocument"]["version"]    = data["version"]
        params["position"]["line"]           = data["line"]
        params["position"]["character"]      = data["column"]

        self.send_request( method, params )

    def _lsp_completion(self, data: dict):
        method = "textDocument/completion"
        params = completion_request["params"]

        params["textDocument"]["uri"]        = data["uri"]
        params["position"]["line"]           = data["line"]
        params["position"]["character"]      = data["column"]

        self.send_request( method, params )

    def _lsp_java_class_file_contents(self, uri: str):
        method = "java/classFileContents"
        params = {
            "uri": uri
        }

        self.send_request( method, params )
