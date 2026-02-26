# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .code.code_container import CodeContainer
from ..widgets.save_file_dialog import SaveFileDialog
from ..widgets.controls.open_files_button import OpenFilesButton



class CenterContainer(Gtk.Box):
    def __init__(self):
        super(CenterContainer, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.ctx = self.get_style_context()
        self.ctx.add_class("center-container")

        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_hexpand(True)
        self.set_vexpand(True)


    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        widget_registery.expose_object("center-container", self)

        SaveFileDialog()
        OpenFilesButton()

        self.add( CodeContainer() )
