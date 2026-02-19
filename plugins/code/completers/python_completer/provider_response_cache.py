# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GObject
from gi.repository import GtkSource

import jedi
from jedi.api import Script

# Application imports
from libs.event_factory import Code_Event_Types

from core.widgets.code.completion_providers.provider_response_cache_base import ProviderResponseCacheBase



# FIXME: Find real icon names...
icon_names = {
    'import':    '',
    'module':    '',
    'class':     '',
    'function':  '',
    'statement': '',
    'param':     ''
}


class Jedi:
    def get_script(file, doc_text):
        return Script(code = doc_text, path = file)



class ProviderResponseCache(ProviderResponseCacheBase):
    def __init__(self):
        super(ProviderResponseCache, self).__init__()

        self._file  = None


    def process_file_load(self, event: Code_Event_Types.AddedNewFileEvent):
        ...

    def process_file_close(self, event: Code_Event_Types.RemovedFileEvent):
        ...

    def process_file_save(self, event: Code_Event_Types.SavedFileEvent):
        ...

    def process_file_change(self, event: Code_Event_Types.TextChangedEvent):
        ...

    def filter(self, word: str) -> list[dict]:
        response: list[dict] = []

        return response

    def filter_with_context(self, context: GtkSource.CompletionContext) -> list[dict]:
        response: list[dict] = []

        if not self._file: return response

        itr       = self.get_iter_correctly(context)
        buffer    = itr.get_buffer()

        doc_text    = buffer.get_text(
            buffer.get_start_iter(),
            buffer.get_end_iter(),
            False
        )
        iter_cursor = buffer.get_iter_at_mark( buffer.get_insert() )
        linenum     = iter_cursor.get_line() + 1
        charnum     = iter_cursor.get_line_index()

        def create_generator():
            if not self._file: return []

            for completion in Jedi.get_script(self._file, doc_text).complete(
                line   = linenum,
                column = None,
                fuzzy  = False
            ):
                {
                    "label": completion.name,
                    "text":  completion.name,
                    "info":  completion.docstring()
                    "icon"   self.get_icon_for_type(completion.type)
                }

                yield comp_item

        for item in create_generator():
            response.append(item)

        return response

    def get_icon_for_type(self, _type):
        try:
            return self._theme.load_icon(icon_names[_type.lower()], 16, 0)
        except (KeyError, AttributeError, GObject.GError) as e:
            return self._theme.load_icon(Gtk.STOCK_ADD, 16, 0)
        except (GObject.GError, AttributeError) as e:
            return None
