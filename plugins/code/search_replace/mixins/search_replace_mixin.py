# Python imports

# Lib imports
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

# Application imports
from .search_mixin import SearchMixin
from .replace_mixin import ReplaceMixin



class SearchReplaceMixin(SearchMixin, ReplaceMixin):

    def _find_entry_focus_in_event(self, entry, event):
        search_text = entry.get_text()
        buffer      = self.active_view.get_buffer()

        if buffer.get_has_selection() and not search_text:
            if not self.mode_bttn_box.in_selection:
                start_itr, end_itr = buffer.get_selection_bounds()

                entry.set_text(
                    buffer.get_text(
                        start_itr,
                        end_itr,
                        include_hidden_chars = False
                    )
                )

            return

    def _find_entry_search_change(self, entry):
        search_text        = entry.get_text()
        buffer             = self.active_view.get_buffer()
        self.highlight_tag = buffer.get_tag_table().lookup("search-highlight")

        if not search_text:
            self.update_style(-1)
            self.clear_highlight(buffer)
            self.status_lbl.set_label("Find in current buffer...")
            return

        self._find_all_matches(search_text, buffer)
        self._highlight_all_matches(buffer)
        self._update_status_lbl(len(self.matches), search_text)

    def _find_entry_activate(self, entry):
        self._find_entry_next_match(entry)

    def _find_entry_next_match(self, entry):
        search_text = entry.get_text()

        if not search_text: return

        buffer = self.active_view.get_buffer()
        self._search_for_next_word(buffer)

    def _find_entry_previous_match(self, entry):
        search_text = entry.get_text()

        if not search_text: return

        buffer = self.active_view.get_buffer()
        self._search_for_prev_word(buffer)

    def _replace_entry_activate(self, entry):
        to_text = entry.get_text()

        if not to_text: return

        buffer  = self.active_view.get_buffer()
        self._replace_word(self.current_index, to_text, buffer)
        self._find_entry_search_change(self.find_entry)

    def _replace_all_activate(self, entry):
        to_text = entry.get_text()

        if not to_text: return

        buffer  = self.active_view.get_buffer()
        self._replace_all_words(to_text, buffer)

    def _highlight_current(self, current_index, buffer):
        self.clear_highlight(buffer)

        start_itr, end_itr = self.matches[current_index]
        buffer.apply_tag(self.highlight_tag, start_itr, end_itr)

        self.active_view.scroll_to_iter(end_itr, 0.2, False, 0, 0)
