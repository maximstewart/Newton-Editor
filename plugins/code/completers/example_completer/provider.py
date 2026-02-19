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
        This is a custom Completion Example Provider.
        # NOTE: used information from here --> https://warroom.rsmus.com/do-that-auto-complete/
    """
    __gtype_name__ = 'ExampleCompletionProvider'

    def __init__(self):
        super(Provider, self).__init__()

        self.response_cache: ProviderResponseCache = ProviderResponseCache()


    def do_get_name(self):
        """ Returns: a new string containing the name of the provider. """
        return 'Example Code Completion'

    def do_match(self, context):
        # Note: If provider is in interactive activation then need to check
        # view focus as otherwise non focus views start trying to grab it.
        completion = context.get_property("completion")
        if not completion.get_view().has_focus(): return

        word = self.response_cache.get_word(context)
        if not word or len(word) < 2: return False
        return True

    def do_get_priority(self):
        """ Determin position in result list along other providor results. """
        return 5

    def do_activate_proposal(self, proposal, iter_):
        """ Manually handle actual completion insert or set flags and handle normally. """

        buffer = iter_.get_buffer()
        # Note: Flag mostly intended for SourceViewsMultiInsertState
        #       to insure marker processes inserted text correctly.
        buffer.is_processing_completion = True
        return False

    def do_get_activation(self):
        """ The context for when a provider will show results """
    #     return GtkSource.CompletionActivation.NONE
    #     return GtkSource.CompletionActivation.USER_REQUESTED
    #     return GtkSource.CompletionActivation.USER_REQUESTED | GtkSource.CompletionActivation.INTERACTIVE
        return GtkSource.CompletionActivation.INTERACTIVE

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

