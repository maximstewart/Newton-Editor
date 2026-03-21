# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#from gi.repository import GLib

# Application imports



class EditorsContainer(Gtk.Paned):
    def __init__(self, code_base: any):
        super(EditorsContainer, self).__init__()

        self.code_base = code_base

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.ctx = self.get_style_context()
        self.ctx.add_class("paned-editors-container")

        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_wide_handle(True)

    def _setup_signals(self):
        self.connect("map", self._init_map)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        self.scrolled_win1, \
        self.scrolled_win2 = self._create_views()

        self.pack1( self.scrolled_win1, True, True )
        self.pack2( self.scrolled_win2, True, True )

    def _create_views(self):
        scrolled_win1 = Gtk.ScrolledWindow()
        scrolled_win2 = Gtk.ScrolledWindow()

        source_view1  = self.code_base.create_source_view()
        source_view2  = self.code_base.create_source_view()

        source_view1.sibling_right = source_view2
        source_view2.sibling_left  = source_view1

        scrolled_win1.add( source_view1 )
        scrolled_win2.add( source_view2 )

        return scrolled_win1, scrolled_win2

    def _init_map(self, view):
        self.disconnect_by_func( self._init_map )
        self.code_base.first_map_load()
        self.code_base = None
        del self.code_base
