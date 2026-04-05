# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .editors_container import EditorsContainer



class CodeContainer(Gtk.Box):
    def __init__(self):
        super(CodeContainer, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.ctx = self.get_style_context()
        self.ctx.add_class("code-container")

        self.set_orientation(Gtk.Orientation.VERTICAL)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        widget_registery.expose_object("code-container", self)
        self.add( EditorsContainer() )
