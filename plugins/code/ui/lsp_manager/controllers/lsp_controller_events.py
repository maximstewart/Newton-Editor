# Python imports
import os

# Lib imports
from gi.repository import GLib

# Application imports
from libs.dto.code.lsp.lsp_messages import get_message_obj
from libs.dto.code.lsp.lsp_messages import didopen_notification
from libs.dto.code.lsp.lsp_messages import didsave_notification
from libs.dto.code.lsp.lsp_messages import didclose_notification
from libs.dto.code.lsp.lsp_messages import didchange_notification
from libs.dto.code.lsp.lsp_messages import completion_request
from libs.dto.code.lsp.lsp_messages import definition_request
from libs.dto.code.lsp.lsp_messages import references_request
from libs.dto.code.lsp.lsp_messages import symbols_request



class LSPControllerEvents:
    def send_initialize_message(self, init_ops: dict, workspace_file: str, workspace_uri: str):
        folder_name = os.path.basename(workspace_file)

        self._init_params["processId"]        = None
        self._init_params["rootPath"]         = workspace_file
        self._init_params["rootUri"]          = workspace_uri
        self._init_params["workspaceFolders"] = [
            {
                "name": folder_name,
                "uri": workspace_uri
            }
        ]

        self._init_params["initializationOptions"] = init_ops
        self.send_request("initialize", self._init_params)

    def send_initialized_message(self):
        self.send_notification("initialized")

    def _lsp_did_open(self, data: dict):
        method = "textDocument/didOpen"
        params = didopen_notification["params"]

        params["textDocument"]["uri"]        = data["uri"]
        params["textDocument"]["languageId"] = data["language_id"]
        params["textDocument"]["text"]       = data["text"]

        GLib.idle_add( self.send_notification, method, params )

    def _lsp_did_save(self, data: dict):
        method = "textDocument/didSave"
        params = didsave_notification["params"]

        params["textDocument"]["uri"] = data["uri"]
        params["text"]                = data["text"]

        GLib.idle_add( self.send_notification, method, params )

    def _lsp_did_close(self, data: dict):
        method = "textDocument/didClose"
        params = didclose_notification["params"]

        params["textDocument"]["uri"] = data["uri"]

        GLib.idle_add( self.send_notification, method, params )

    def _lsp_did_change(self, data: dict):
        method = "textDocument/didChange"
        params = didchange_notification["params"]

        params["textDocument"]["uri"]        = data["uri"]
        params["textDocument"]["languageId"] = data["language_id"]
        params["textDocument"]["version"]    = data["version"]

        contentChanges         = params["contentChanges"][0]
        contentChanges["text"] = data["text"]

        GLib.idle_add( self.send_notification, method, params )

    # def _lsp_did_change(self, data: dict):
    #     method = "textDocument/didChange"
    #     params = didchange_notification_range["params"]

    #     params["textDocument"]["uri"]        = data["uri"]
    #     params["textDocument"]["languageId"] = data["language_id"]
    #     params["textDocument"]["version"]    = data["version"]

    #     contentChanges         = params["contentChanges"][0]
    #     start                  = contentChanges["range"]["start"]
    #     end                    = contentChanges["range"]["end"]
    #     contentChanges["text"] = data["text"]
    #     start["line"]          = data["line"]
    #     start["character"]     = 0
    #     end["line"]            = data["line"]
    #     end["character"]       = data["column"]

    #     GLib.idle_add( self.send_notification, method, params )

    def _lsp_definition(self, data: dict):
        method = "textDocument/definition"
        params = definition_request["params"]

        params["textDocument"]["uri"]        = data["uri"]
        params["textDocument"]["languageId"] = data["language_id"]
        params["textDocument"]["version"]    = data["version"]
        params["position"]["line"]           = data["line"]
        params["position"]["character"]      = data["column"]

        GLib.idle_add( self.send_request, method, params )

    def _lsp_completion(self, data: dict):
        method = "textDocument/completion"
        params = completion_request["params"]

        params["textDocument"]["uri"]        = data["uri"]
        params["textDocument"]["languageId"] = data["language_id"]
        params["textDocument"]["version"]    = data["version"]
        params["position"]["line"]           = data["line"]
        params["position"]["character"]      = data["column"]

        GLib.idle_add( self.send_request, method, params )
