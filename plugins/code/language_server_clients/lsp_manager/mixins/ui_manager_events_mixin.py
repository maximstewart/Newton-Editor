# Python imports

# Lib imports
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import GLib
from gi.repository import Gtk

# Application imports



class UIManagerEventsMixin:
    def _setup_signals(self):
        self.connect("show", self._handle_show)
        self.connect("destroy", self._handle_destroy)

    def _subscribe_to_events(self):
        ...

    def _handle_show(self, widget):
        GLib.idle_add(self.path_entry.grab_focus)

    def _handle_destroy(self, widget):
        self.disconnect_by_func(self._handle_show)
        self.disconnect_by_func(self._handle_destroy)
        self.path_bttn.disconnect_by_func(self._file_set)
        self.combo_box.disconnect_by_func(self._on_combo_changed)
        self.hide_bttn.disconnect(self.hide_bttn_id)
        self.create_client_bttn.disconnect_by_func(self._create_client)
        self.close_client_bttn.disconnect_by_func(self._close_client)

    def _map_resize(self, widget, parent):
        parent_x,     \
        parent_y      = parent.get_position()
        parent_width, \
        parent_height = parent.get_size()

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

    def _on_combo_changed(self, combo: Gtk.ComboBoxText):
        lang_id = combo.get_active_text()
        self.set_source_view_text( self.path_entry.get_text() )

