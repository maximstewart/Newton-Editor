# Python imports
from concurrent.futures import ThreadPoolExecutor

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GLib
from gi.repository import GtkSource

# Application imports
from libs.event_factory import Code_Event_Types

from core.widgets.code.completion_providers.provider_response_cache_base import ProviderResponseCacheBase



class ProviderResponseCache(ProviderResponseCacheBase):
    def __init__(self):
        super(ProviderResponseCache, self).__init__()

        self.matchers: dict = {}


    def process_file_load(self, event: Code_Event_Types.AddedNewFileEvent):
        buffer = event.file.buffer
        with ThreadPoolExecutor(max_workers = 1) as executor:
            executor.submit(self._handle_change, buffer)

    def process_file_close(self, event: Code_Event_Types.RemovedFileEvent):
        self.matchers[event.file.buffer] = set()
        del self.matchers[event.file.buffer]

    def process_file_save(self, event: Code_Event_Types.SavedFileEvent):
        ...

    def process_file_change(self, event: Code_Event_Types.TextChangedEvent):
        buffer = event.file.buffer
        with ThreadPoolExecutor(max_workers = 1) as executor:
            executor.submit(self._handle_change, buffer)

    def _handle_change(self, buffer):
        start_itr = buffer.get_start_iter()
        end_itr   = buffer.get_end_iter()
        data      = buffer.get_text(start_itr, end_itr, False)
 
        if not data:
            GLib.idle_add(self.load_empty_set, buffer)
            return

        if not buffer in self.matchers:
            GLib.idle_add(self.load_as_new_set, buffer, data)
            return

        new_words = self.get_all_words(data)
        GLib.idle_add(self.load_into_set, buffer, new_words)

    def filter(self, word: str) -> list[dict]:
        response: list[dict] = []

        for entry in self.matchers:
            if not word in entry: continue
            data = self.matchers[entry]
            response.append(data)

        return response

    def filter_with_context(self, context: GtkSource.CompletionContext) -> list[dict]:
        buffer = self.get_iter_correctly(context).get_buffer()
        word   = self.get_word(context).rstrip()

        if not buffer in self.matchers:
            self.matchers[buffer] = set()

        response: list[dict] = []
        for entry in self.matchers[buffer]:
            if not entry.rstrip().startswith(word): continue

            data = {
                "label": entry,
                "text": entry,
                "info": ""
            }

            response.append(data)

        return response

    def load_empty_set(self, buffer):
        self.matchers[buffer] = set()

    def load_into_set(self, buffer, new_words):
        self.matchers[buffer].update(new_words)

    def load_as_new_set(self, buffer, data):
        self.matchers[buffer] = self.get_all_words(data)

    def get_all_words(self, data: str):
        words = set()

        def is_word_char(c):
            return c.isalnum() or c == '_'

        size = len(data)
        i = 0
        
        while i < size:
            # Skip non-word characters
            while i < size and not is_word_char(data[i]):
                i += 1

            start = i
            # Consume word characters
            while i < size and is_word_char(data[i]):
                i += 1

            word = data[start:i]
            if not word: continue
            words.add(word)

        return words
