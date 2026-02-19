# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk

# Application imports
from .mixins.search_replace_mixin import SearchReplaceMixin

from .mode_buttons import ModeButtons



class SearchReplace(Gtk.Grid, SearchReplaceMixin):
    def __init__(self):
        super(SearchReplace, self).__init__()

        self.active_view          = None
        self.highlight_tag        = None
        self.matches: list[tuple] = []

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()

        self.show_all()
        self.hide()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("search-replace")

        self.set_hexpand(True)
        self.set_column_spacing(15)
        self.set_row_spacing(15)
        self.set_row_spacing(15)

        self.set_margin_start(15)
        self.set_margin_end(15)
        self.set_margin_top(15)
        self.set_margin_bottom(15)

    def _setup_signals(self):
        self.connect("show", self._handle_show)
        self.connect("hide", self._handle_hide)

    def _load_widgets(self):
        self.stateus_lbl      = Gtk.Label(label = "Find in Current Buffer")
        self.find_options_lbl = Gtk.Label(label = "Finding with Options: Case Insensitive")
        self.mode_bttn_box    = ModeButtons()

        self.find_entry       = Gtk.SearchEntry()
        self.replace_entry    = Gtk.SearchEntry()
        find_bttn             = Gtk.Button(label = "Find")
        find_all_bttn         = Gtk.Button(label = "Find All")
        replace_bttn          = Gtk.Button(label = "Replace")
        replace_all_bttn      = Gtk.Button(label = "Replace All")

        self.find_entry.set_hexpand(True)
        self.replace_entry.set_hexpand(True)
        self.find_entry.set_max_width_chars(16)
        self.replace_entry.set_max_width_chars(16)
        self.find_entry.set_placeholder_text("Find in current buffer...")
        self.replace_entry.set_placeholder_text("Replace in current buffer...")

        self.mode_bttn_box.request_update = self.request_update

        self.find_entry.connect("focus-in-event", self._find_entry_focus_in_event)
        self.find_entry.connect("key-release-event", self._find_entry_key_release_event)
        self.find_entry.connect("activate", self._find_entry_activate)
        self.find_entry.connect("search-changed", self._find_entry_search_change)
        self.find_entry.connect("next-match", self._find_entry_next_match)
        self.find_entry.connect("previous-match", self._find_entry_previous_match)

        self.replace_entry.connect("key-release-event", self._replace_entry_key_release_event)
        self.replace_entry.connect("activate", self._replace_entry_activate)

        find_bttn.connect(
            "clicked",
            lambda button: self._find_entry_next_match(self.find_entry)
        )
        find_all_bttn.connect(
            "clicked",
            lambda button: self._find_entry_search_change(self.find_entry)
        )
        replace_bttn.connect(
            "clicked",
            lambda button: self._replace_entry_activate(self.replace_entry)
        )
        replace_all_bttn.connect(
            "clicked",
            lambda button: self._replace_all_activate(self.replace_entry) 
        )

        self.attach(child = self.stateus_lbl,      left = 0, top = 0, width = 2, height = 1)
        self.attach(child = self.find_options_lbl, left = 2, top = 0, width = 2, height = 1)
        self.attach(child = self.mode_bttn_box,    left = 4, top = 0, width = 2, height = 1)

        self.attach(child = self.find_entry,       left = 0, top = 1, width = 4, height = 1)
        self.attach(child = find_bttn,             left = 4, top = 1, width = 1, height = 1)
        self.attach(child = find_all_bttn,         left = 5, top = 1, width = 1, height = 1)

        self.attach(child = self.replace_entry,    left = 0, top = 2, width = 4, height = 1)
        self.attach(child = replace_bttn,          left = 4, top = 2, width = 1, height = 1)
        self.attach(child = replace_all_bttn,      left = 5, top = 2, width = 1, height = 1)

    def _handle_show(self, widget):
        self.find_entry.set_text("")
        self.find_entry.grab_focus()

    def _handle_hide(self, widget):
        if not self.active_view: return

        buffer = self.active_view.get_buffer()
        self.clear_highlight(buffer)
        self.active_view.grab_focus()

    def request_update(self):
        self._find_entry_search_change(self.find_entry)

    def _find_entry_key_release_event(self, widget, event):
        modifiers  = Gdk.ModifierType(event.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        is_control = True if modifiers & Gdk.ModifierType.CONTROL_MASK else False
        is_shift   = True if modifiers & Gdk.ModifierType.SHIFT_MASK else False
        keyname    = Gdk.keyval_name(event.keyval).lower()

        if is_control and keyname == "f":
            self.hide()
        elif is_control and keyname == "r":
            self.replace_entry.grab_focus()

    def _replace_entry_key_release_event(self, widget, event):
        modifiers  = Gdk.ModifierType(event.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        is_control = True if modifiers & Gdk.ModifierType.CONTROL_MASK else False
        is_shift   = True if modifiers & Gdk.ModifierType.SHIFT_MASK else False
        keyname    = Gdk.keyval_name(event.keyval).lower()

        if is_control and keyname == "l":
            self.find_entry.grab_focus()
        elif is_control and keyname == "f":
            self.hide()

    def clear_highlight(self, buffer):
        if not self.highlight_tag: return
        start, end = buffer.get_bounds()
        buffer.remove_tag(self.highlight_tag, start, end)

