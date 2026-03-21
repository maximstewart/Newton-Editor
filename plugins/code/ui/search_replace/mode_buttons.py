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
        self.connect("destroy", self._handle_destroy)

    def _load_widgets(self):
        self.use_regex_bttn    = Gtk.ToggleButton(label = ".*")
        self.match_case_bttn   = Gtk.ToggleButton(label = "Aa")
        self.in_selection_bttn = Gtk.ToggleButton()
        self.whole_word_bttn   = Gtk.ToggleButton()
        self.hide_bttn         = Gtk.Button(label = "X")

        self.use_regex_bttn.set_sensitive(False)

        self.use_regex_bttn.set_tooltip_text("Use Regex")
        self.match_case_bttn.set_tooltip_text("Match Case")
        self.in_selection_bttn.set_tooltip_text("Only In Selection")
        self.whole_word_bttn.set_tooltip_text("Whole Word")

        self.use_regex_bttn.connect("toggled", self._toggled_button, "use_regex")
        self.match_case_bttn.connect("toggled", self._toggled_button, "match_case")
        self.in_selection_bttn.connect("toggled", self._toggled_button, "in_selection")
        self.whole_word_bttn.connect("toggled", self._toggled_button, "whole_word")

        self.hide_bttn_id = self.hide_bttn.connect(
            "clicked",
            lambda widget: self.get_parent().hide()
        )

        self.in_selection_bttn.set_image(
            Gtk.Image.new_from_file("images/only-in-selection.png")
        )
        self.whole_word_bttn.set_image(
            Gtk.Image.new_from_file("images/whole-word.png")
        )

        self.add(self.use_regex_bttn)
        self.add(self.match_case_bttn)
        self.add(self.in_selection_bttn)
        self.add(self.whole_word_bttn)
        self.add(self.hide_bttn)

    def _toggled_button(self, toggle_button, mode: str):
        setattr(self, mode, not getattr(self, mode))
        self.request_update()

    def request_update(self):
        raise ModeException("Must by 'monkey' patched from search_replace.py") 

    def _handle_destroy(self, widget):
        self.disconnect_by_func(self._handle_destroy)

        self.use_regex_bttn.disconnect_by_func(self._toggled_button)
        self.match_case_bttn.disconnect_by_func(self._toggled_button)
        self.in_selection_bttn.disconnect_by_func(self._toggled_button)
        self.whole_word_bttn.disconnect_by_func(self._toggled_button)

        self.hide_bttn.disconnect(self.hide_bttn_id)
