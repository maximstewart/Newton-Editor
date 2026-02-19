# Python imports
from contextlib import suppress

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class SearchMixin:
    def is_word_char(self, ch):
        return ch.isalnum() or ch == "_"

    def is_whole_word(self, start_itr, end_itr, buffer):
        if start_itr.backward_char():
            prev_char = start_itr.get_char()
            if self.is_word_char(prev_char):
                return False

        # if end_itr.forward_char():
        #     next_char = end_itr.get_char()
        #     if self.is_word_char(next_char):
        #         return False
        next_char = end_itr.get_char()
        if self.is_word_char(next_char):
            return False

        return True


    def _find_all_matches(self, search_text, buffer):
        self.update_style(0)

        self.matches.clear()
        self.current_index = -1

        start_itr   = buffer.get_start_iter()
        end_itr     = buffer.get_end_iter()

        case_mode   = Gtk.TextSearchFlags.CASE_INSENSITIVE if not self.mode_bttn_box.match_case else Gtk.TextSearchFlags.TEXT_ONLY 
        whole_word  = self.mode_bttn_box.whole_word
        if self.mode_bttn_box.in_selection:
            with suppress(Exception):
                start_itr, end_itr = buffer.get_selection_bounds()

        while True:
            match = start_itr.forward_search(
                search_text,
                case_mode,
                end_itr
            )

            if not match: break

            match_start, match_end = match
            if whole_word and not self.is_whole_word(match_start.copy(), match_end.copy(), buffer):
                start_itr = match_end
                continue

            self.matches.append(
                (match_start.copy(), match_end.copy())
            )

            start_itr = match_end

    def _highlight_all_matches(self, buffer):
        self.clear_highlight(buffer)

        for start_itr, end_itr in self.matches:
            buffer.apply_tag(self.highlight_tag, start_itr, end_itr)

    def _search_for_next_word(self, buffer):
        self.current_index = (self.current_index + 1) % len(self.matches)
        self._highlight_current(self.current_index, buffer)

    def _search_for_prev_word(self, buffer):
        self.current_index = (self.current_index - 1) % len(self.matches)
        self._highlight_current(self.current_index, buffer)
