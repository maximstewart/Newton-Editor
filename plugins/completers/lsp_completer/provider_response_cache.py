# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from libs.event_factory import Code_Event_Types

from core.widgets.code.completion_providers.provider_response_cache_base import ProviderResponseCacheBase



class ProviderResponseCache(ProviderResponseCacheBase):
    def __init__(self):
        super(ProviderResponseCache, self).__init__()


    def process_file_load(self, event: Code_Event_Types.AddedNewFileEvent):
        ...

    def process_file_close(self, event: Code_Event_Types.RemovedFileEvent):
        ...

    def process_file_save(self, event: Code_Event_Types.SavedFileEvent):
        ...

    def process_file_change(self, event: Code_Event_Types.TextChangedEvent):
        ...

    def filter(self, word: str) -> list[dict]:
        return []

    def filter_with_context(self, context: GtkSource.CompletionContext)  -> list[dict]:
        proposals = [
            {
                "label": "LSP Class",
                "text": "LSP Code",
                "info": "A test LSP completion item..."
            }
        ]

        return proposals
