# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

# Application imports



class Telescope(Gtk.Window):
    def __init__(self):
        super(Telescope, self).__init__(Gtk.WindowType.POPUP)

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_decorated(False)
        self.set_modal(False)
        self.set_destroy_with_parent(True)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_size_request(620, 480)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)

    def _setup_signals(self):
#        self.connect("page-added", self._page_added)
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        main_box     = Gtk.Box()
        left_box     = Gtk.Box()
        list_box     = Gtk.ListBox()
        search_entry = Gtk.SearchEntry()

        left_box.set_orientation(Gtk.Orientation.VERTICAL)
        list_box.set_vexpand(True)
        list_box.set_size_request(120, -1)

        left_box.add(list_box)
        left_box.add(search_entry)
        main_box.add(left_box)
        self.add(main_box)

        main_box.show_all()

