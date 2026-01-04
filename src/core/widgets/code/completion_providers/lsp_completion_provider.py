# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import Gtk
from gi.repository import GtkSource
from gi.repository import GObject

# Application imports



class LSPCompletionProvider(GObject.Object, GtkSource.CompletionProvider):
    """
        This code is an LSP code completion plugin for Newton.
        # NOTE: Some code pulled/referenced from here --> https://github.com/isamert/gedi
    """
    __gtype_name__ = 'LSPProvider'

    def __init__(self):
        GObject.Object.__init__(self)

        self._icon_theme = Gtk.IconTheme.get_default()

        self.lsp_data = None


    def pre_populate(self, context):
        ...

    def do_get_name(self):
        return "LSP Code Completion"

    def get_iter_correctly(self, context):
        return context.get_iter()[1] if isinstance(context.get_iter(), tuple) else context.get_iter()

    def do_match(self, context):
        iter = self.get_iter_correctly(context)
        iter.backward_char()

        buffer = iter.get_buffer()
        if buffer.get_context_classes_at_iter(iter) != ['no-spell-check']:
            return False

        ch = iter.get_char()
        # NOTE: Look to re-add or apply supprting logic to use spaces
         # As is it slows down the editor in certain contexts...
        # if not (ch in ('_', '.', ' ') or ch.isalnum()):
        if not (ch in ('_', '.') or ch.isalnum()):
            return False

        return True

    def do_get_priority(self):
        return 5

    def do_populate(self, context, items = []):
        # self.lsp_data
        proposals = []

        comp_item = GtkSource.CompletionItem.new()
        comp_item.set_label("LSP Class")
        comp_item.set_text("LSP Code")
        # comp_item.set_icon(self.get_icon_for_type(completion.type))
        comp_item.set_info("A test LSP completion item...")

        context.add_proposals(self, [comp_item], True)














    # def do_populate(self, context, items = []):
    #     if hasattr(self._source_view, "completion_items"):
    #         items = self._source_view.completion_items

    #     proposals = []
    #     for item in items:
    #         proposals.append( self.create_completion_item(item) )

    #     context.add_proposals(self, proposals, True)

    # def get_icon_for_type(self, _type):
    #     try:
    #         return self._theme.load_icon(icon_names[_type.lower()], 16, 0)
    #     except:
    #         ...

    #     try:
    #         return self._theme.load_icon(Gtk.STOCK_ADD, 16, 0)
    #     except:
    #         ...

    #     return None

    # def create_completion_item(self, item):
    #     comp_item = GtkSource.CompletionItem.new()
    #     keys      = item.keys()
    #     comp_item.set_label(item["label"])

    #     if "insertText" in keys:
    #         comp_item.set_text(item["insertText"])

    #     if "additionalTextEdits" in keys:
    #         comp_item.additionalTextEdits = item["additionalTextEdits"]

    #     return comp_item


    # def create_completion_item(self, item):
    #     comp_item = GtkSource.CompletionItem.new()
    #     comp_item.set_label(item.label)

    #     if item.textEdit:
    #         if isinstance(item.textEdit, dict):
    #             comp_item.set_text(item.textEdit["newText"])
    #         else:
    #             comp_item.set_text(item.textEdit)
    #     else:
    #         comp_item.set_text(item.insertText)

    #     comp_item.set_icon( self.get_icon_for_type(item.kind) )
    #     comp_item.set_info(item.documentation)

    #     return comp_item