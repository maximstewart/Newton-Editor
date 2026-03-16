# Python imports
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

        self.client_configs: dict[str, str] = {}

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
        self.path_bttn.set_halign(Gtk.Align.FILL)

        self.path_bttn.connect("file-set", self._file_set)
        self.combo_box.connect("changed", self._on_combo_changed)
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
            self.path_bttn.unselect_all()
            self.path_bttn.emit("file-set")
            buttons_widget.hide()
            return

        self.set_source_view_text( self.path_entry.get_text() )
        buttons_widget.show()

    def _file_set(self, widget):
        fname = widget.get_filename()
        fname = "" if not fname else fname
        self.path_entry.set_text(fname)

        lang_id = self.combo_box.get_active_text()
        if not lang_id or lang_id not in self.client_configs: return

        self.set_source_view_text(
            "{workspace.folder}" if not fname else fname
        )

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

    def _on_combo_changed(self, combo: Gtk.ComboBoxText):
        lang_id = combo.get_active_text()
        self.set_source_view_text( self.path_entry.get_text() )


    def set_source_view_text(self, workspace_dir: str):
        lang_id  = self.combo_box.get_active_text()
        if not lang_id: return

        json_str = self.client_configs[lang_id].replace("{workspace.folder}", workspace_dir)
        buffer   = self.source_view.get_buffer()

        buffer.set_text(json_str, -1)

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

    def add_client_listing(self, lang_id: str, lang_config: str):
        self.combo_box.append_text(lang_id)
        self.client_configs[lang_id] = lang_config

    def get_init_opts(self, lang_id: str) -> dict:
        if not lang_id or lang_id not in self.client_configs: return {}

        try:
            lang_config = json.loads(self.client_configs[lang_id])
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON for {lang_id}: {e}")
            return {}

        return lang_config.get("initialization-options", {})

    def toggle_client_buttons(self, show_close: bool):
        self.create_client_bttn.set_visible(not show_close)
        self.close_client_bttn.set_visible(show_close)
