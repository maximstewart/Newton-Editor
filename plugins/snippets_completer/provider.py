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



class Provider(GObject.GObject, GtkSource.CompletionProvider):
    """
        This is a Snippits Completion Provider.
        # NOTE: used information from here --> https://warroom.rsmus.com/do-that-auto-complete/
    """
    __gtype_name__ = 'SnippetsCompletionProvider'

    def __init__(self):
        GObject.Object.__init__(self)

        self.response_cache: ProviderResponseCache = ProviderResponseCache()


    def do_get_name(self):
        return 'Snippits Completion'

    def do_match(self, context):
        word = self.response_cache.get_word(context)
        if not word or len(word) < 2: return False

        return True

    def do_get_priority(self):
        return 2

    def do_get_activation(self):
        """ The context for when a provider will show results """
        # return GtkSource.CompletionActivation.NONE
        return GtkSource.CompletionActivation.USER_REQUESTED
        # return GtkSource.CompletionActivation.INTERACTIVE

    def do_populate(self, context):
        word      = self.response_cache.get_word(context)
        results   = self.response_cache.filter(word)
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
