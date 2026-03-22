# Python imports
import sys
import os


BASE_DIR = os.path.dirname( os.path.realpath(__file__) )
LIBS_DIR = f"{BASE_DIR}/libs"

if str(LIBS_DIR) not in sys.path:
    sys.path.insert(0, LIBS_DIR)


# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

import tree_sitter_language_pack as tslp



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.TextChangedEvent):
            if not tslp.has_language( event.file.ftype ):
                try:
                    tslp.download( [event.file.ftype] )
                except Exception:
                    logger.info(
                        f"Tree Sitter Language Pack:\nCouldn't download -> '{event.file.ftype}' language type..."
                    )
                    return

            buffer = event.file.buffer
            start_itr, \
            end_itr    = buffer.get_bounds()
            text       = buffer.get_text(start_itr, end_itr, True)
            result     = tslp.process(
                text,
                tslp.ProcessConfig(
                    language = event.file.ftype
                )
            )

            event.file.tree_sitter_meta = result

    def load(self):
        tslp.configure(
            cache_dir = f"{BASE_DIR}/cache/tree-sitter-language-pack/v1.0.0/libs"
        )

    def unload(self):
        ...

    def run(self):
        # tslp.download(
        #     [
        #         "python",
        #         "java",
        #         "go",
        #         "c",
        #         "cpp",
        #         "javascript",
        #         "html",
        #         "css",
        #         "json"
        #     ]
        # )
        #         "gdscript"

        ...
