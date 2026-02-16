# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class TabWidget(Gtk.Box):
    """docstring for TabWidget"""

    def __init__(self):
        super(TabWidget, self).__init__()

        self._close_tab = None

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("tab-widget")

        self.set_orientation(0)
        self.set_hexpand(False)

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        self.label     = Gtk.Label()
        self.close_btn = Gtk.Button()
        icon           = Gtk.Image(stock = Gtk.STOCK_CLOSE)

        ctx = self.label.get_style_context()
        ctx.add_class("tab-label")
        ctx = self.close_btn.get_style_context()
        ctx.add_class("tab-close-bttn")

        self.label.set_xalign(0.0)
        self.label.set_margin_left(25)
        self.label.set_margin_right(25)
        self.label.set_hexpand(True)

        self.close_btn.add(icon)
        self.add(self.label)
        self.add(self.close_btn)

        self.show_all()

    def clear_signals_and_data(self):
        self.close_btn.disconnect(self._handler_id)
        self._close_tab    = None
        self._handler_id   = None

        for child in self.get_children():
            child.unparent()
            child.run_dispose()
            child.destroy()

    def set_close_signal(self, callback):
        self._handler_id = self.close_btn.connect(
            'button-release-event',
            callback,
            self.file
        )
