# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..widgets.separator_widget import Separator
from ..widgets.vte_widget import VteWidget



class FooterContainer(Gtk.Box):
    def __init__(self):
        super(FooterContainer, self).__init__()


        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.ctx = self.get_style_context()
        self.ctx.add_class("footer-container")

        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_hexpand(True)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        widget_registery.expose_object("footer-container", self)

        vte_widget = VteWidget()

        vte_widget.hide()
        self.add( vte_widget )

        self.add( Separator("separator-footer", 0) )
