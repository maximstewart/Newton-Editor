# Python imports
from concurrent.futures import ThreadPoolExecutor
import re

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GtkSource

# Application imports
from libs.event_factory import Code_Event_Types

from core.widgets.code.completion_providers.provider_response_cache_base import ProviderResponseCacheBase



class ProviderResponseCache(ProviderResponseCacheBase):
    def __init__(self):
        super(ProviderResponseCache, self).__init__()

        # Note: Using asyncio.run causes a keyboard trap that prevents app
        # closure from terminal. ThreadPoolExecutor seems to not have such issues...
        self.executor = ThreadPoolExecutor(max_workers = 1)
        self.matchers: dict = {
            "hello": {
                "label": "Hello, World!",
                "text": "Hello, World!",
                "info": GLib.markup_escape_text( "<b>Says the first ever program developers write...</b>" )
            },
            "foo": {
                "label": "foo",
                "text": "foo }}"
            },
            "bar": {
                "label": "bar",
                "text": "bar }}"
            }
        }


    def process_file_load(self, event: Code_Event_Types.AddedNewFileEvent):
        ...

    def process_file_close(self, event: Code_Event_Types.RemovedFileEvent):
        ...

    def process_file_save(self, event: Code_Event_Types.SavedFileEvent):
        ...

    def process_file_text_inserted(self, event: Code_Event_Types.TextInsertedEvent):
        ...

    def process_file_delete_range(self, event: Code_Event_Types.DeleteRangeEvent):
        ...

    def filter(self, word: str) -> list[dict]:
        ...

    def filter_with_context(self, context) -> list[dict]:
        """
            In this instance, it will do 2 things:
                1) always provide Hello World! (Not ideal but an option so its in the example)
                2) Utilizes the Gtk.TextIter from the TextBuffer to determine if there is a jinja
                    example of '{{ custom.' if so it will provide you with the options of foo and bar.
            If selected it will insert foo }} or bar }}, completing your syntax...

            PLEASE NOTE the GtkTextIter Logic and regex are really rough and should be adjusted and tuned
        """

        proposals: list[dict] = [
            {
                "label": self.matchers[ "hello" ]["label"],
                "text":  self.matchers[ "hello" ]["text"],
                "info":  self.matchers[ "hello" ]["info"]
            }
        ]

        # Gtk Versions differ on get_iter responses...
        end_iter = context.get_iter()
        if not isinstance(end_iter, Gtk.TextIter):
            _, end_iter = context.get_iter()

        if not end_iter: return

        buf = end_iter.get_buffer()
        mov_iter = end_iter.copy()
        if mov_iter.backward_search('{{', Gtk.TextSearchFlags.VISIBLE_ONLY):
            mov_iter, _ = mov_iter.backward_search('{{', Gtk.TextSearchFlags.VISIBLE_ONLY)
            left_text = buf.get_text(mov_iter, end_iter, True)
        else:
            left_text = ''

        if re.match(r'.*\{\{\s*custom\.$', left_text):
            # optionally proposed based on left search via regex
            proposals.append(
                {
                    "label": self.matchers[ "foo" ]["label"],
                    "text":  self.matchers[ "foo" ]["text"],
                    "info":  ""
                }
            )

            # optionally proposed based on left search via regex
            proposals.append(
                {
                    "label": self.matchers[ "bar" ]["label"],
                    "text":  self.matchers[ "bar" ]["text"],
                    "info":  ""
                }
            )

        return proposals
