# Python imports
from os import path
import json

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GtkSource

# Application imports



class LSPManagerUI(Gtk.Dialog):
    __gsignals__ = {
        'create-client': (GObject.SignalFlags.RUN_LAST, None, (str, str)),
        'close-client': (GObject.SignalFlags.RUN_LAST, None, (str,)),
    }

    def __init__(self):
        super(LSPManagerUI, self).__init__()

        self._SCRIPT_PTH: str          = path.dirname( path.realpath(__file__) )
        self._USER_HOME: str           = path.expanduser('~')
        self._LSP_SERVERS_CONFIG: str  = ""
        self.servers_config: dict      = {}

        self.parent                    = None
        self.source_view               = None

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_modal(True)
        self.set_decorated(False)
        self.set_vexpand(True)
        self.set_hexpand(True)

    def _setup_signals(self):
        self.connect("show", self._show)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        content_area       = self.get_content_area()
        self.main_box      = Gtk.Grid()
        self.path_entry    = Gtk.SearchEntry()
        self.path_bttn     = Gtk.FileChooserButton.new(
            title  = "Workspace Folder",
            action = Gtk.FileChooserAction.SELECT_FOLDER
        )
        self.combo_box     = Gtk.ComboBoxText()

        self.hide_bttn     = Gtk.Button(label = "X")
        bttn_box           = Gtk.Box()
        self.create_client_bttn = Gtk.Button(label = "Create Language Client")
        self.close_client_bttn  = Gtk.Button(label = "Close Language Client")

        self.path_entry.set_can_focus(False)
        self.path_entry.set_placeholder_text("Workspace Folder...")
        self.path_entry.connect("changed", self._path_changed, bttn_box)

        self.path_bttn.connect("file-set", self._file_set)
        self.path_bttn.set_halign(Gtk.Align.FILL)
        self.hide_bttn.connect("clicked", lambda widget: self.hide())
        self.create_client_bttn.connect("clicked", self._create_client, self.close_client_bttn)
        self.close_client_bttn.connect("clicked", self._close_client, self.create_client_bttn)

        self.main_box.set_column_spacing(15)
        self.main_box.set_row_spacing(15)

        bttn_box.pack_start(self.create_client_bttn, False, False, 0)
        bttn_box.pack_start(self.close_client_bttn, False, False, 0)

        self.main_box.attach(child = self.path_entry, left = 0, top = 0, width = 4, height = 1)
        self.main_box.attach(child = self.path_bttn,  left = 4, top = 0, width = 1, height = 1)
        self.main_box.attach(child = self.combo_box,  left = 5, top = 0, width = 1, height = 1)
        self.main_box.attach(child = self.hide_bttn,  left = 6, top = 0, width = 1, height = 1)
        self.main_box.attach(child = bttn_box,        left = 0, top = 1, width = 1, height = 1)

        content_area.set_vexpand(True)
        content_area.set_hexpand(True)

        content_area.add(self.main_box)
        content_area.show_all()
        self.close_client_bttn.hide()
        bttn_box.hide()

    def _show(self, widget):
        GLib.idle_add(self.path_entry.grab_focus)

    def _map_resize(self, widget, parent):
        parent_x, parent_y = parent.get_position()
        parent_width, parent_height = parent.get_size()
        if parent_width == 0 or parent_height == 0: return

        width  = int(parent_width  * 0.75)
        height = int(parent_height * 0.75)

        widget.resize(width, height)

        x = parent_x + (parent_width - width)   // 2
        y = parent_y + (parent_height - height) // 2
        widget.move(x, y)

    def _path_changed(self, widget, buttons_widget):
        if not widget.get_text():
            buttons_widget.hide()
            return

        buttons_widget.show()

    def _file_set(self, widget):
        self.path_entry.set_text(
            widget.get_filename()
        )
        self.load_lsp_servers_config_placeholders()

    def map_parent_resize_event(self, parent):
        parent.connect("size-allocate", lambda w, r: self._map_resize(self, parent))

    def set_source_view(self, source_view):
        scrolled_win     = Gtk.ScrolledWindow()
        lang_manager     = GtkSource.LanguageManager()
        buffer           = source_view.get_buffer()
        language         = lang_manager.get_language("json")
        self.source_view = source_view

        buffer.set_language(language)
        buffer.set_style_scheme(self.source_view.syntax_theme)

        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)

        scrolled_win.add(self.source_view)
        self.main_box.attach(child = scrolled_win, left = 0, top = 2, width = 7, height = 1)

        scrolled_win.show_all()

    def load_lsp_servers_config(self):
        try:
            with open(f"{self._SCRIPT_PTH}/configs/lsp-servers-config.json") as file:
                self._LSP_SERVERS_CONFIG = file.read()
        except FileNotFoundError:
            logger.error(f"Config file not found: {self._SCRIPT_PTH}/configs/lsp-servers-config.json")

    def load_lsp_servers_config_placeholders(self):
        if not self._LSP_SERVERS_CONFIG: return
        if not self.source_view: return

        data = self._LSP_SERVERS_CONFIG \
                .replace("{user.home}", self._USER_HOME) \
                .replace("{workspace.folder}", self.path_entry.get_text())

        self.servers_config = json.loads(data)

        buffer     = self.source_view.get_buffer()
        start_itr, \
        end_itr    = buffer.get_bounds()

        buffer.delete(start_itr, end_itr)
        buffer.insert(start_itr, data, -1)

        self.set_language_combo_box( list(self.servers_config.keys()) )

    def set_language_combo_box(self, lang_ids: list[str]):
        self.combo_box.remove_all()

        for lang_id in lang_ids:
            self.combo_box.append_text(lang_id)

    def get_init_opts(self, lang_id: str) -> dict:
        buffer = self.source_view.get_buffer()
        try:
            self.servers_config = json.loads(
                buffer.get_text( *buffer.get_bounds() )
            )
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            return {}

        if not lang_id or not lang_id in self.servers_config: return {}

        return self.servers_config[lang_id].get("initialization-options", {})

    def _create_client(self, widget, sibling):
        if not self.source_view: return

        buffer  = self.source_view.get_buffer()
        lang_id = self.combo_box.get_active_text()

        if not lang_id: return

        workspace_dir = self.path_entry.get_text()
        self.emit('create-client', lang_id, workspace_dir)

    def _close_client(self, widget, sibling):
        lang_id = self.combo_box.get_active_text()

        if not lang_id: return
        self.emit('close-client', lang_id)

    def toggle_client_buttons(self, show_close: bool):
        self.create_client_bttn.set_visible(not show_close)
        self.close_client_bttn.set_visible(show_close)
