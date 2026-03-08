# Python imports
import json

# Lib imports

# Application imports
from .lsp_message_structs import MessageEncoder



LEN_HEADER  = "Content-Length: "
TYPE_HEADER = "Content-Type: "



def get_message_str(data: dict) -> str:
    return json.dumps(data, separators = (',', ':'), indent = 4, cls = MessageEncoder)

def get_message_obj(data: str):
    return json.loads(data)



# Request type formatting
# https://github.com/microsoft/multilspy/blob/main/src/multilspy/language_server.py#L417
content_part = {
	"method": "textDocument/definition",
	"params": {
	    "textDocument": {
            "uri": "file://",
            "languageId": "python",
            "version": 1,
            "text": ""
	    },
	    "position": {
	        "line": 5,
            "character": 12,
            "offset": 0
	    }
	}
}


didopen_notification = {
	"method": "textDocument/didOpen",
	"params": {
	    "textDocument": {
            "uri": "file://",
            "languageId": "python",
            "version": 1,
            "text": ""
	    }
	}
}

didsave_notification = {
	"method": "textDocument/didSave",
	"params": {
	    "textDocument": {
            "uri": "file://"
	    },
        "text": ""
	}
}

didclose_notification = {
	"method": "textDocument/didClose",
	"params": {
	    "textDocument": {
            "uri": "file://"
	    }
	}
}


didchange_notification = {
	"method": "textDocument/didChange",
	"params": {
	    "textDocument": {
            "uri": "file://",
            "languageId": "python",
            "version": 1,
	    },
	    "contentChanges": [
	        {
	            "text": ""
	        }
	    ]
	}
}

didchange_notification_range = {
	"method": "textDocument/didChange",
	"params": {
	    "textDocument": {
            "uri": "file://",
            "languageId": "python",
            "version": 1,
            "text": ""
	    },
	    "contentChanges": [
	        {
	            "range": {
	                "start": {
	                    "line": 1,
                        "character": 1,
	                },
	                "end": {
	                    "line": 1,
                        "character": 1,
	                },
	                "rangeLength": 0
	            }
	        }
	    ]
	}
}


# CompletionTriggerKind = 1 | 2 | 3;
# export const Invoked: 1 = 1;
# export const TriggerCharacter: 2 = 2;
# export const TriggerForIncompleteCompletions: 3 = 3;
completion_request = {
	"method": "textDocument/completion",
	"params": {
	    "textDocument": {
            "uri": "file://",
            "languageId": "python",
            "version": 1,
            "text": ""
	    },
	    "position": {
	        "line": 5,
            "character": 12,
            "offset": 0
	    },
	    "contet": {
	        "triggerKind": 3,
	        "triggerCharacter": ""
	    }
	}
}

definition_request = {
	"method": "textDocument/definition",
	"params": {
	    "textDocument": {
            "uri": "file://",
            "languageId": "python",
            "version": 1,
            "text": ""
	    },
	    "position": {
	        "line": 5,
            "character": 12,
            "offset": 0
	    }
	}
}

references_request = {
    "method": "textDocument/references",
    "params": {
        "context": {
            "includeDeclaration": False
        },
	    "textDocument": {
            "uri": "file://",
            "languageId": "python",
            "version": 1,
            "text": ""
	    },
	    "position": {
	        "line": 30,
            "character": 13,
            "offset": 0
	    }
	}
}


symbols_request = {
	"method": "textDocument/documentSymbol",
	"params": {
	    "textDocument": {
            "uri": "file://",
            "languageId": "python",
            "version": 1,
            "text": ""
	    }
	}
}