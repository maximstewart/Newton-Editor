# Python imports
from os import path

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GLib
from gi.repository import GtkSource

# Application imports
from libs.event_factory import Code_Event_Types

from core.widgets.code.completion_providers.provider_response_cache_base import ProviderResponseCacheBase

from . import cson



class ProviderResponseCache(ProviderResponseCacheBase):
    def __init__(self):
        super(ProviderResponseCache, self).__init__()

        self.matchers: dict = {}

        self.load_snippets()


    def load_snippets(self):
        fpath = path.join(path.dirname(path.realpath(__file__)), "snippets.cson")
        with open(fpath, 'rb') as f:
            self.snippets = cson.load(f)
            for group in self.snippets:
                self.snippets[group]
                for entry in self.snippets[group]:
                    data = self.snippets[group][entry]
                    self.matchers[ data["prefix"] ] = {
                        "label": entry,
                        "text": data["body"],
                        "info": GLib.markup_escape_text( data["body"] )
                    }

    def process_file_load(self, event: Code_Event_Types.AddedNewFileEvent):
        ...

    def process_file_close(self, event: Code_Event_Types.RemovedFileEvent):
        ...

    def process_file_save(self, event: Code_Event_Types.SavedFileEvent):
        ...

    def process_file_change(self, event: Code_Event_Types.TextChangedEvent):
        ...

    def filter(self, word: str):
        response: list = []

        for entry in self.matchers:
            if not word in entry: continue
            data = self.matchers[entry]
            response.append(data)

        return response

    def filter_with_context(self, context: GtkSource.CompletionContext):
        ...
