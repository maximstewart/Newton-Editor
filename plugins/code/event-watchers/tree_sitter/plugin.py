# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .tree_sitter import Parser, get_parser



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def set_ast(self, file):
        if not hasattr(file, "tree_sitter"):
            parser = get_parser( file.ftype )
            if not parser: return

            file.tree_sitter = parser

        buffer     = file.buffer
        start_itr, \
        end_itr    = buffer.get_bounds()
        text       = buffer.get_text(start_itr, end_itr, True)

        tree = file.tree_sitter.parse( text.encode("UTF-8") )
        file.ast = tree

    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.FocusedViewEvent):
            self.view = event.view
            event = Event_Factory.create_event(
                "get_file", buffer = self.view.get_buffer()
            )
            self.emit_to("files", event)

            file = event.response

            if not file: return
            if file.ftype == "buffer": return

            self.set_ast(file)
        elif isinstance(event, Code_Event_Types.TextChangedEvent):
            self.set_ast(event.file)

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
