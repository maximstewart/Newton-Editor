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



class ProviderResponseCache(ProviderResponseCacheBase):
    def __init__(self):
        super(ProviderResponseCache, self).__init__()

        self.matchers: dict = {}


    def process_file_load(self, event: Code_Event_Types.AddedNewFileEvent):
        self.load_as_new_set(event.file.buffer)

    def process_file_close(self, event: Code_Event_Types.RemovedFileEvent):
        self.matchers[event.file.buffer] = []
        del self.matchers[event.file.buffer]

    def process_file_save(self, event: Code_Event_Types.SavedFileEvent):
        ...

    def process_file_change(self, event: Code_Event_Types.TextChangedEvent):
        buffer = event.file.buffer
        # if self.get_if_in_matched_word_set(buffer): return
        self.load_as_new_set(buffer)


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


    def load_as_new_set(self, buffer):
        start_itr = buffer.get_start_iter()
        end_itr   = buffer.get_end_iter()
        data      = buffer.get_text(start_itr, end_itr, False)

        if not data:
            self.matchers[buffer] = set()
            return

        self.matchers[buffer] = self.get_all_words(data)

    def get_if_in_matched_word_set(self, buffer):
        was_found = False

        if not buffer in self.matchers: return was_found

        insert_itr = buffer.get_iter_at_mark( buffer.get_insert() )
        end_itr    = insert_itr.copy()
        start_itr  = end_itr.copy()

        if not start_itr.starts_word():
            start_itr.backward_word_start()

        if not end_itr.ends_word():
            end_itr.forward_word_end()

        word      = buffer.get_text(start_itr, end_itr, False)
        for _word in self.matchers[buffer]:
            if not _word.startswith(word): continue
            was_found = True

        if was_found: return was_found

        self.matchers[buffer].add(word)

        return was_found


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
