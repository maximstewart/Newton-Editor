# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango
from gi.repository import Gio

# Application imports



class InfoBarWidget(Gtk.Box):
    """ docstring for InfoBarWidget. """

    def __init__(self):
        super(InfoBarWidget, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_margin_start(25)
        self.set_margin_end(25)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...


    def _load_widgets(self):
        self.path_label      = Gtk.Label(label = "...")
        self.line_char_label = Gtk.Label(label = "1:0")
        self.encoding_label  = Gtk.Label(label = "utf-8")
        self.file_type_label = Gtk.Label(label = "buffer")

        self.add(self.path_label)
        self.add(self.line_char_label)
        self.add(self.encoding_label)
        self.add(self.file_type_label)

        self.path_label.set_hexpand(True)
        self.path_label.set_ellipsize(Pango.EllipsizeMode.START)
        self.path_label.set_single_line_mode(True)
        self.path_label.set_max_width_chars(48)

        self.line_char_label.set_hexpand(True)
        self.encoding_label.set_hexpand(True)
        self.file_type_label.set_hexpand(True)

    def _set_info_labels(
        self,
        path: Gio.File or str = None,
        line_char: str        = None,
        file_type: str        = None,
        encoding_type: str    = None
    ):
        self._set_path_label(path)
        self._set_line_char_label(line_char)
        self._set_file_type_label(file_type)
        self._set_encoding_label(encoding_type)

    def _set_path_label(self, gfile: Gio.File or str = "..."):
        gfile = "" if not gfile else gfile

        if isinstance(gfile, str):
            self.path_label.set_text( gfile )
            self.path_label.set_tooltip_text( gfile )
        else:
            self.path_label.set_text( gfile.get_path() )
            self.path_label.set_tooltip_text( gfile.get_path() )

    def _set_line_char_label(self, line_char = "1:1"):
        line_char = "1:1" if not line_char else line_char

        self.line_char_label.set_text(line_char)

    def _set_file_type_label(self, file_type = "buffer"):
        file_type = "buffer" if not file_type else file_type 

        self.file_type_label.set_text(file_type)

    def _set_encoding_label(self, encoding_type = "utf-8"):
        encoding_type = "utf-8" if not encoding_type else encoding_type

        self.encoding_label.set_text(encoding_type)


