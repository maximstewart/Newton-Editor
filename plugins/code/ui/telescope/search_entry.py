# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import GLib

# Application imports
from .list_box import ListBox



class TelescopeSearchEntryException(Exception):
    ...



class SearchEntry(Gtk.SearchEntry):
    def __init__(self):
        super(SearchEntry, self).__init__()


        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        self.connect("search-changed", self._search_changed)
        self.connect("key-press-event", self._key_press_event)
        self.connect("key-release-event", self._key_release_event)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def _key_press_event(self, widget, eve):
        modifiers  = Gdk.ModifierType(eve.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        is_control = modifiers & Gdk.ModifierType.CONTROL_MASK
        is_shift   = modifiers & Gdk.ModifierType.SHIFT_MASK
        keyname    = Gdk.keyval_name(eve.keyval).lower()
        char_str   = chr( Gdk.keyval_to_unicode(eve.keyval) )

        if keyname == "up":
            self.move_row_selection_up()
            return True
        elif keyname == "down":
            self.move_row_selection_down()
            return True


    def _key_release_event(self, widget, eve):
        modifiers  = Gdk.ModifierType(eve.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        is_control = modifiers & Gdk.ModifierType.CONTROL_MASK
        is_shift   = modifiers & Gdk.ModifierType.SHIFT_MASK
        keyname    = Gdk.keyval_name(eve.keyval).lower()
        char_str   = chr( Gdk.keyval_to_unicode(eve.keyval) )

        if is_control:
            if char_str == "b":
                self.hide()

            return True

        if keyname in ["enter", "return"]:
            self.activate_row()
            self.hide()

            return True

    def _search_changed(self, widget):
        self.search_changed(widget)

    def hide(self):
        raise TelescopeSearchEntryException("SearchEntry must have 'hide' monkey patched...")

    def search_changed(self, widget):
        raise TelescopeSearchEntryException("SearchEntry must have 'search_changed' monkey patched...")

    def activate_row(self):
        raise TelescopeSearchEntryException("SearchEntry must have 'activate_row' monkey patched...")

    def move_row_selection_up(self):
        raise TelescopeSearchEntryException("SearchEntry must have 'move_row_selection_up' monkey patched...")

    def move_row_selection_down(self):
        raise TelescopeSearchEntryException("SearchEntry must have 'move_row_selection_down' monkey patched...")

