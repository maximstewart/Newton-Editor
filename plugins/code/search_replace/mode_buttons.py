# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class ModeException(Exception):
    ...



class ModeButtons(Gtk.ButtonBox):
    def __init__(self):
        super(ModeButtons, self).__init__()

        self.use_regex: bool    = False
        self.match_case: bool   = False
        self.in_selection: bool = False
        self.whole_word: bool   = False

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("search-replace-mode-buttons")

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        use_regex_bttn    = Gtk.ToggleButton(label = ".*")
        match_case_bttn   = Gtk.ToggleButton(label = "Aa")
        in_selection_bttn = Gtk.ToggleButton()
        whole_word_bttn   = Gtk.ToggleButton()

        use_regex_bttn.set_sensitive(False)

        use_regex_bttn.set_tooltip_text("Use Regex")
        match_case_bttn.set_tooltip_text("Match Case")
        in_selection_bttn.set_tooltip_text("Only In Selection")
        whole_word_bttn.set_tooltip_text("Whole Word")

        use_regex_bttn.connect("toggled", self._toggled_button, "use_regex")
        match_case_bttn.connect("toggled", self._toggled_button, "match_case")
        in_selection_bttn.connect("toggled", self._toggled_button, "in_selection")
        whole_word_bttn.connect("toggled", self._toggled_button, "whole_word")

        in_selection_bttn.set_image(
            Gtk.Image.new_from_file("images/only-in-selection.png")
        )
        whole_word_bttn.set_image(
            Gtk.Image.new_from_file("images/whole-word.png")
        )

        self.add(use_regex_bttn)
        self.add(match_case_bttn)
        self.add(in_selection_bttn)
        self.add(whole_word_bttn)

    def _toggled_button(self, toggle_button, mode: str):
        setattr(self, mode, not getattr(self, mode))
        self.request_update()

    def request_update(self):
        raise ModeException("Must by 'monkey' patched from search_replace.py") 


