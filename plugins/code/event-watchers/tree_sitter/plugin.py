# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .tree_sitter import Parser, get_parser



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.TextChangedEvent):
            if not hasattr(event.file, "tree_sitter"):
                parser = get_parser( event.file.ftype )
                if not parser: return

                event.file.tree_sitter = parser

            buffer     = event.file.buffer
            start_itr, \
            end_itr    = buffer.get_bounds()
            text       = buffer.get_text(start_itr, end_itr, True)

            tree = event.file.tree_sitter.parse( text.encode("UTF-8") )
            event.file.ast = tree

#            root = tree.root_node
#            print("Root type:", root.type)
#            for child in root.children:
#                print(child.type, child.start_point, child.end_point)

    def load(self):
        ...

    def unload(self):
        ...

    def run(self):
        ...
