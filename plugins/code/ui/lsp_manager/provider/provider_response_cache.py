# Python imports
from concurrent.futures import ThreadPoolExecutor

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from libs.dto.code.lsp.lsp_message_structs import LSPResponseTypes, LSPResponseRequest, LSPResponseNotification

from core.widgets.code.completion_providers.provider_response_cache_base import ProviderResponseCacheBase



class ProviderResponseCache(ProviderResponseCacheBase):
    def __init__(self):
        super(ProviderResponseCache, self).__init__()

        self.matchers: dict = {}
        self._lsp_client = None

    def set_lsp_client(self, lsp_client):
        self._lsp_client = lsp_client

    def process_file_load(self, event):
        if self._lsp_client:
            self._lsp_client.process_file_load(event)

    def process_file_close(self, event):
        if self._lsp_client:
            self._lsp_client.process_file_close(event)

    def process_file_save(self, event):
        if self._lsp_client:
            self._lsp_client.process_file_save(event)

    def process_file_change(self, event):
        if self._lsp_client:
            self._lsp_client.process_file_change(event)

    def filter(self, word: str) -> list[dict]:
        return []

    def filter_with_context(self, context: GtkSource.CompletionContext)  -> list[dict]:
        return list( self.matchers.values() )
