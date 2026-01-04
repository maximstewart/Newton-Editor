# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

# Application imports
from ...widgets.code.view import SourceView



class PanedEditorsContainer(Gtk.Paned):
    def __init__(self):
        super(PanedEditorsContainer, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.ctx = self.get_style_context()
        self.ctx.add_class("paned-editors-container")

        self.set_hexpand(True)
        self.set_vexpand(True)
        # self.set_homogeneous(True)
        self.set_wide_handle(True)

    def _setup_signals(self):
        self.map_id = self.connect("map", self._init_map)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        scrolled_win1 = Gtk.ScrolledWindow()
        scrolled_win2 = Gtk.ScrolledWindow()
        source_view1  = SourceView()
        source_view2  = SourceView()

        source_view1.sibling_right = source_view2
        source_view2.sibling_left  = source_view1

        scrolled_win1.add( source_view1 )
        scrolled_win2.add( source_view2 )

        self.add1(scrolled_win1)
        self.add2(scrolled_win2)

    def _init_map(self, view):
        def _first_show_init():
            self.disconnect(self.map_id)
            del self.map_id

            self._handle_first_show()

            return False

        GLib.timeout_add(250, _first_show_init)

    def _handle_first_show(self):
        self.set_position(
            self.get_allocated_width() / 2
        )

