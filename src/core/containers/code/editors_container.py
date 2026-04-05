# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from core.widgets.code.code_base import CodeBase
from core.widgets.separator_widget import Separator



class EditorsContainer(Gtk.Box):
    def __init__(self):
        super(EditorsContainer, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.ctx = self.get_style_context()
        self.ctx.add_class("editors-container")

        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_size_request(320, -1)

    def _setup_signals(self):
        self.connect("map", self._init_map)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        box            = Gtk.Box()
        widget_registery.expose_object("editors-container", self)
        self.code_base = CodeBase()
        scrolled_win,  \
        source_view    = self.code_base.create_source_view()

        box.add( scrolled_win )
        self.add( Separator("separator_left") )
        self.add( box )
        self.add( Separator("separator_right") )

    def _init_map(self, view):
        self.disconnect_by_func( self._init_map )
        self.code_base.first_map_load()
        del self.code_base
