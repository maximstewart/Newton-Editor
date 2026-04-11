# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from core.widgets.code.completion_providers.provider_response_cache_base import ProviderResponseCacheBase



class ProviderResponseCache(ProviderResponseCacheBase):
    def __init__(self):
        super(ProviderResponseCache, self).__init__()

        self.matchers: dict     = {}
        self.lsp_manager_client = None

    def set_lsp_manager_client(self, lsp_client):
        self.lsp_manager_client = lsp_client

    def process_file_load(self, event):
        if self.lsp_manager_client:
            self.lsp_manager_client.process_file_load(event)

    def process_file_close(self, event):
        if self.lsp_manager_client:
            self.lsp_manager_client.process_file_close(event)

    def process_file_save(self, event):
        if self.lsp_manager_client:
            self.lsp_manager_client.process_file_save(event)

    def process_file_text_inserted(self, event):
        if self.lsp_manager_client:
            self.lsp_manager_client.process_file_text_inserted(event)

    def process_file_delete_range(self, event):
        if self.lsp_manager_client:
            self.lsp_manager_client.process_file_delete_range(event)

    def filter(self, word: str) -> list[dict]:
        return []

    def filter_with_context(self, context: GtkSource.CompletionContext)  -> list[dict]:
        return list( self.matchers.values() )
