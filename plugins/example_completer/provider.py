# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GtkSource
from gi.repository import GObject

# Application imports
from .provider_response_cache import ProviderResponseCache



class Provider(GObject.GObject, GtkSource.CompletionProvider):
    """
        This is a custom Completion Example Provider.
        # NOTE: used information from here --> https://warroom.rsmus.com/do-that-auto-complete/
    """
    __gtype_name__ = 'ExampleCompletionProvider'

    def __init__(self):
        GObject.Object.__init__(self)

        self.response_cache: ProviderResponseCache = ProviderResponseCache()


    def do_get_name(self):
        """ Returns: a new string containing the name of the provider. """
        return 'Example Completion'

    def do_match(self, context):
        # word = context.get_word()
        # if not word or len(word) < 2: return False

        """ Get whether the provider match the context of completion detailed in context. """
        word = self.response_cache.get_word(context)
        if not word or len(word) < 2: return False

        return True

    def do_get_priority(self):
        """ Determin position in result list along other providor results. """
        return 5

    def do_get_activation(self):
        """ The context for when a provider will show results """
    #     return GtkSource.CompletionActivation.NONE
    #     return GtkSource.CompletionActivation.USER_REQUESTED
    #     return GtkSource.CompletionActivation.USER_REQUESTED | GtkSource.CompletionActivation.INTERACTIVE
        return GtkSource.CompletionActivation.INTERACTIVE

    def do_populate(self, context):
        proposals = self.response_cache.filter_with_context(context)

        context.add_proposals(self, proposals, True)

