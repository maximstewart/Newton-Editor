# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GObject
from gi.repository import GtkSource

# Application imports
from .provider_response_cache import ProviderResponseCache



class Provider(GObject.GObject, GtkSource.CompletionProvider):
    """
        This code is an LSP code completion plugin for Newton.
        # NOTE: Some code pulled/referenced from here --> https://github.com/isamert/gedi
    """
    __gtype_name__ = 'LSPProvider'

    def __init__(self):
        super(Provider, self).__init__()

        self.response_cache: ProviderResponseCache = None


    def pre_populate(self, context):
        ...

    def do_get_name(self):
        return "LSP Code Completion"

    def do_match(self, context):
        # Note: If provider is in interactive activation then need to check
        # view focus as otherwise non focus views start trying to grab it.
        # completion = context.get_property("completion")
        # if not completion.get_view().has_focus(): return

        iter = self.response_cache.get_iter_correctly(context)
        iter.backward_char()
        ch = iter.get_char()

        # NOTE: Look to re-add or apply supporting logic to use spaces
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

    def do_activate_proposal(self, proposal, iter_):
        buffer = iter_.get_buffer()
        # Note: Flag mostly intended for SourceViewsMultiInsertState
        #       to insure marker processes inserted text correctly.
        buffer.is_processing_completion = True
        return False

    def do_get_activation(self):
        """ The context for when a provider will show results """
#        return GtkSource.CompletionActivation.NONE
        return GtkSource.CompletionActivation.USER_REQUESTED
#        return GtkSource.CompletionActivation.INTERACTIVE

    def do_populate(self, context):
        results   = self.response_cache.filter_with_context(context)
        proposals = []

        for entry in results:
            proposals.append(
                self.response_cache.create_completion_item(
                    entry["label"],
                    entry["text"],
                    entry["info"]
                )
            )

        context.add_proposals(self, proposals, True)
