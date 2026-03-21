# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

# Application imports
from .list_box import ListBox
from .search_entry import SearchEntry



class Telescope(Gtk.Dialog):
    def __init__(self):
        super(Telescope, self).__init__()

        self.source_view = None

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_modal(False)
        self.set_decorated(False)
        self.set_vexpand(True)
        self.set_hexpand(True)

    def _setup_signals(self):
        self.connect("focus-out-event", self._focus_out_event)
        self.connect("show", self._show)
        self.connect("destroy", self._handle_destroy)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        content_area      = self.get_content_area()
        self.main_box     = Gtk.Box()
        left_box          = Gtk.Box()

        self.list_box     = ListBox()
        self.list_box.set_buffer  = self.set_buffer

        self.search_entry = SearchEntry()

        self.search_entry.hide                    = self._focus_out_event
        self.search_entry.search_changed          = self.list_box.search_changed
        self.search_entry.activate_row            = self.list_box.activate_row
        self.search_entry.move_row_selection_up   = self.list_box.move_row_selection_up
        self.search_entry.move_row_selection_down = self.list_box.move_row_selection_down

        self.main_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        left_box.set_orientation(Gtk.Orientation.VERTICAL)

        left_box.add(self.list_box)
        left_box.add(self.search_entry)
        self.main_box.pack_start(left_box, False, False, 0)

        content_area.add(self.main_box)
        content_area.show_all()

    def _focus_out_event(self, widget = None, event = None):
        self.hide()

    def _show(self, widget):
        GLib.idle_add(self.search_entry.grab_focus)

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

    def set_emit(self, emit):
        self.list_box.emit = emit

    def set_active_row(self, buffer):
        self.list_box.set_active_row(buffer)

    def set_buffer(self, buffer):
        self.source_view.set_buffer(buffer)

    def map_parent_resize_event(self, parent):
        self.size_allocate_id = parent.connect("size-allocate", lambda w, r: self._map_resize(self, parent))

    def unmap_parent_resize_event(self, parent):
        parent.disconnect(self.size_allocate_id)

    def set_source_view(self, source_view):
        scrolled_win     = Gtk.ScrolledWindow()
        self.source_view = source_view

        scrolled_win.add(self.source_view)
        self.main_box.pack_end(scrolled_win, True, True, 0)

        scrolled_win.show_all()

    def _handle_destroy(self, widget):
        self.disconnect_by_func(self._focus_out_event)
        self.disconnect_by_func(self._show)
        self.disconnect_by_func(self._handle_destroy)
