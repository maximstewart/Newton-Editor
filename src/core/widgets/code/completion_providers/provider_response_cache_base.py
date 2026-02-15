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



class ProviderResponseCacheException(Exception):
    ...



class ProviderResponseCacheBase:
    def __init__(self):
        super(ProviderResponseCacheBase, self).__init__()

        self._icon_theme = Gtk.IconTheme.get_default()


    def process_file_load(self, buffer: GtkSource.Buffer):
        raise ProviderResponseCacheException("ProviderResponseCacheBase 'process_file_load' not implemented...")

    def process_file_close(self, buffer: GtkSource.Buffer):
        raise ProviderResponseCacheException("ProviderResponseCacheBase 'process_file_close' not implemented...")

    def process_file_save(self, buffer: GtkSource.Buffer):
        raise ProviderResponseCacheException("ProviderResponseCacheBase 'process_file_save' not implemented...")

    def process_file_change(self, buffer: GtkSource.Buffer):
        raise ProviderResponseCacheException("ProviderResponseCacheBase 'process_change' not implemented...")

    def filter(self, word: str):
        raise ProviderResponseCacheException("ProviderResponseCacheBase 'filter' not implemented...")

    def filter_with_context(self, context: GtkSource.CompletionContext):
        raise ProviderResponseCacheException("ProviderResponseCacheBase 'filter_with_context' not implemented...")


    def create_completion_item(
        self,
        label: str      = "",
        text: str       = "",
        info: str       = "",
        completion: any = None
    ):
        if not label or not text: return

        comp_item = GtkSource.CompletionItem.new()
        comp_item.set_label(label)
        comp_item.set_text(text)

        if info:
            comp_item.set_info(info)
            # comp_item.set_markup(f"<h3>{info}</h3>")

        if completion:
            comp_item.set_icon(
                self.get_icon_for_type(completion.type)
            )

        return comp_item

    def get_word(self, context):
        start_iter = context.get_iter()
        end_iter   = None

        if not isinstance(start_iter, Gtk.TextIter):
            _, start_iter = context.get_iter()
            end_iter = start_iter.copy()

        if not start_iter.starts_word():
            start_iter.backward_word_start()

        end_iter.forward_word_end()

        buffer = start_iter.get_buffer()

        return buffer.get_text(start_iter, end_iter, False)
