# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class TabWidget(Gtk.Box):
    def __init__(self):
        super(TabWidget, self).__init__()

        self.file = None

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("tab-widget")

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        self._label_eve_box = Gtk.EventBox()
        self.label          = Gtk.Label(label = "")
        self.close_btn      = Gtk.Button(label = "X")

        ctx = self.label.get_style_context()
        ctx.add_class("tab-label")
        ctx = self.close_btn.get_style_context()
        ctx.add_class("tab-close-bttn")

        self.label.set_hexpand(True)

        self._label_eve_box.add(self.label)
        self.add(self._label_eve_box)
        self.add(self.close_btn)

    def clear_signals_and_data(self):
        del self.file
        self._label_eve_box.disconnect(self._label_eve_box_id)
        self.close_btn.disconnect(self.close_btn_id)

    def set_select_signal(self, callback):
        self._label_eve_box_id = self._label_eve_box.connect('button-release-event', callback, self.file)

    def set_close_signal(self, callback):
        self.close_btn_id = self.close_btn.connect('button-release-event', callback, self.file)
