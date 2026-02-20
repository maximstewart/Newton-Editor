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
from libs.event_factory import Code_Event_Types



class ProviderResponseCacheException(Exception):
    ...



class ProviderResponseCacheBase:
    def __init__(self):
        super(ProviderResponseCacheBase, self).__init__()

        self._icon_theme = Gtk.IconTheme.get_default()


    def process_file_load(self, event: Code_Event_Types.AddedNewFileEvent):
        raise ProviderResponseCacheException("ProviderResponseCacheBase 'process_file_load' not implemented...")

    def process_file_close(self, event: Code_Event_Types.RemovedFileEvent):
        raise ProviderResponseCacheException("ProviderResponseCacheBase 'process_file_close' not implemented...")

    def process_file_save(self, event: Code_Event_Types.SavedFileEvent):
        raise ProviderResponseCacheException("ProviderResponseCacheBase 'process_file_save' not implemented...")

    def process_file_change(self, event: Code_Event_Types.TextChangedEvent):
        raise ProviderResponseCacheException("ProviderResponseCacheBase 'process_change' not implemented...")

    def filter(self, word: str) -> list[dict]:
        raise ProviderResponseCacheException("ProviderResponseCacheBase 'filter' not implemented...")

    def filter_with_context(self, context: GtkSource.CompletionContext) -> list[dict]:
        raise ProviderResponseCacheException("ProviderResponseCacheBase 'filter_with_context' not implemented...")


    def create_completion_item(
        self,
        label: str = "",
        text: str  = "",
        info: str  = "",
        icon: any  = None
    ) -> dict:
        if not label or not text: return

        comp_item = GtkSource.CompletionItem.new()
        comp_item.set_label(label)
        comp_item.set_text(text)

        if info:
            comp_item.set_info(info)
            # comp_item.set_markup(f"<h3>{info}</h3>")

        if icon:
            comp_item.set_icon(
                self.get_icon_for_type(icon.type)
            )

        return comp_item

    def get_all_marks(self, buffer) -> list:
        marks: list = []
        iter_ = buffer.get_start_iter()

        while iter_:
            marks = iter_.get_marks()

            for mark in marks:
                if mark and mark not in marks:
                    marks.append(mark)

            if not iter_.forward_char():
                break

        return marks

    def get_all_insert_marks(self, buffer) -> list:
        marks: list = []
        iter_ = buffer.get_start_iter()

        while iter_:
            marks = iter_.get_marks()

            for mark in marks:
                if mark.get_name() and "multi_insert_" in mark.get_name():
                    marks.append(mark)

            if not iter_.forward_char():
                break

        return marks

    def get_word(self, context) -> str:
        start_iter = self.get_iter_correctly(context)
        end_iter   = start_iter.copy()

        if not start_iter.starts_word():
            start_iter.backward_word_start()

        if not end_iter.ends_word():
            end_iter.forward_word_end()

        buffer = start_iter.get_buffer()

        return buffer.get_text(start_iter, end_iter, False)

    def get_iter_correctly(self, context) -> Gtk.TextIter:
        return context.get_iter()[1] if isinstance(context.get_iter(), tuple) else context.get_iter()
