# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GtkSource
from gi.repository import GObject

# Application imports
from .provider_response_cache import ProviderResponseCache



class Provider(GObject.Object, GtkSource.CompletionProvider):
    """
        This code is an LSP code completion plugin for Newton.
        # NOTE: Some code pulled/referenced from here --> https://github.com/isamert/gedi
    """
    __gtype_name__ = 'LSPProvider'

    def __init__(self):
        GObject.Object.__init__(self)

        self.response_cache: ProviderResponseCache = ProviderResponseCache()


    def pre_populate(self, context):
        ...

    def do_get_name(self):
        return "LSP Code Completion"

    def get_iter_correctly(self, context):
        return context.get_iter()[1] if isinstance(context.get_iter(), tuple) else context.get_iter()

    def do_match(self, context):
        word = self.response_cache.get_word(context)
        if not word or len(word) < 2: return False

        iter = self.get_iter_correctly(context)
        iter.backward_char()
        ch = iter.get_char()
        # NOTE: Look to re-add or apply supprting logic to use spaces
         # As is it slows down the editor in certain contexts...
        # if not (ch in ('_', '.', ' ') or ch.isalnum()):
        if not (ch in ('_', '.') or ch.isalnum()):
            return False

        buffer = iter.get_buffer()
        if buffer.get_context_classes_at_iter(iter) != ['no-spell-check']:
            return False

        return True

    def do_get_priority(self):
        return 5

    def do_get_activation(self):
        """ The context for when a provider will show results """
    #     return GtkSource.CompletionActivation.NONE
        return GtkSource.CompletionActivation.USER_REQUESTED
    #     return GtkSource.CompletionActivation.INTERACTIVE

    def do_populate(self, context):
        proposals = self.get_completion_filter(context)

        context.add_proposals(self, proposals, True)

    def get_completion_filter(self, context):
        proposals = [
            self.response_cache.create_completion_item(
                "LSP Class",
                "LSP Code",
                "A test LSP completion item..."
            )
        ]

        return proposals
