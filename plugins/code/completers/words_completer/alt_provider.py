# Python imports
import re

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import GtkSource

# Application imports
from .provider_response_cache import ProviderResponseCache



class Provider(GtkSource.CompletionWords):
    """
        This is a Words Completion Provider.
        # NOTE: used information from here --> https://warroom.rsmus.com/do-that-auto-complete/
    """
    __gtype_name__ = 'WordsCompletionProvider'

    def __init__(self):
        super(Provider, self).__init__()

        self.response_cache: ProviderResponseCache = ProviderResponseCache()


    def do_get_name(self):
        return 'Words Completion'

    def do_match(self, context):
        word = self.response_cache.get_word(context)
        if not word or len(word) < 2: return False
        return True

    def do_get_priority(self):
        return 0

    def do_activate_proposal(self, proposal, iter_):
        buffer = iter_.get_buffer()
        # Note: Flag mostly intended for SourceViewsMultiInsertState
        #       to insure marker processes inserted text correctly.
        buffer.is_processing_completion = True
        return False

    def do_get_activation(self):
        """ The context for when a provider will show results """
        # return GtkSource.CompletionActivation.NONE
        # return GtkSource.CompletionActivation.USER_REQUESTED
        return GtkSource.CompletionActivation.INTERACTIVE
