# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import Gtk
from gi.repository import GtkSource

# Application imports
from ..config import get_lsp_host_addr, get_lsp_host_port



class UIManagerSetupMixin:
    def _setup_styling(self):
        self.set_modal(True)
        self.set_decorated(False)
        self.set_vexpand(True)
        self.set_hexpand(True)

    def _load_widgets(self):
        content_area        = self.get_content_area()
        self.main_box       = Gtk.Grid()
        self.path_entry     = Gtk.SearchEntry()
        self.path_bttn      = Gtk.FileChooserButton.new(
            title  = "Workspace Folder",
            action = Gtk.FileChooserAction.SELECT_FOLDER
        )
        self.combo_box      = Gtk.ComboBoxText()
        self.hide_bttn      = Gtk.Button(label = "X")

        self.adddress_entry = Gtk.Entry()
        adjustment = Gtk.Adjustment(
            value          = get_lsp_host_port(),
            lower          = 1,
            upper          = 65535,
            step_increment = 1,
            page_increment = 10,
            page_size      = 0
        )

        self.adddress_port = Gtk.SpinButton()
        self.adddress_port.set_adjustment(adjustment)
        self.adddress_port.set_digits(0)  # integers only

        bttn_box                = Gtk.Box()
        self.create_client_bttn = Gtk.Button(label = "Create Language Client")
        self.close_client_bttn  = Gtk.Button(label = "Close Language Client")

        self.path_entry.set_can_focus(False)
        self.path_entry.set_placeholder_text("Workspace Folder...")
        self.path_entry.connect("changed", self._path_changed, bttn_box)
        self.path_bttn.set_halign(Gtk.Align.FILL)

        self.adddress_entry.set_placeholder_text("Address...")
        self.adddress_entry.set_text( get_lsp_host_addr() )

        self.path_bttn.connect("file-set", self._file_set)
        self.combo_box.connect("changed", self._on_combo_changed)
        self.hide_bttn_id = self.hide_bttn.connect("clicked", lambda widget: self.hide())
        self.create_client_bttn.connect("clicked", self._create_client, self.close_client_bttn)
        self.close_client_bttn.connect("clicked", self._close_client, self.create_client_bttn)

        self.main_box.set_column_spacing(15)
        self.main_box.set_row_spacing(15)

        bttn_box.pack_start(self.create_client_bttn, False, False, 0)
        bttn_box.pack_start(self.close_client_bttn, False, False, 0)

        self.main_box.attach(child = self.path_entry,     left = 0, top = 0, width = 4, height = 1)
        self.main_box.attach(child = self.path_bttn,      left = 4, top = 0, width = 1, height = 1)
        self.main_box.attach(child = self.combo_box,      left = 5, top = 0, width = 1, height = 1)
        self.main_box.attach(child = self.hide_bttn,      left = 6, top = 0, width = 1, height = 1)

        self.main_box.attach(child = self.adddress_entry, left = 0, top = 1, width = 2, height = 1)
        self.main_box.attach(child = self.adddress_port,  left = 2, top = 1, width = 2, height = 1)
        self.main_box.attach(child = bttn_box,            left = 4, top = 1, width = 3, height = 1)

        content_area.set_vexpand(True)
        content_area.set_hexpand(True)

        content_area.add(self.main_box)
        content_area.show_all()
        self.close_client_bttn.hide()
        bttn_box.hide()

    def set_source_view(self, scrolled_win, source_view):
        lang_manager     = GtkSource.LanguageManager()
        buffer           = source_view.get_buffer()
        language         = lang_manager.get_language("json")
        self.source_view = source_view

        buffer.set_language(language)
        buffer.set_style_scheme(self.source_view.syntax_theme)

        self.main_box.attach(scrolled_win, 0, 2, 7, 1)
