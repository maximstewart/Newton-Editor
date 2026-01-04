# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..widgets.controls.transparency_scale import TransparencyScale



class HeaderContainer(Gtk.Box):
    def __init__(self):
        super(HeaderContainer, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.ctx = self.get_style_context()
        self.ctx.add_class("header-container")

        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_hexpand(True)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("tggl-top-main-menubar", self.tggl_top_main_menubar)

    def _load_widgets(self):
        self.add( TransparencyScale() )

    def tggl_top_main_menubar(self):
        self.hide() if self.is_visible() else self.show_all()