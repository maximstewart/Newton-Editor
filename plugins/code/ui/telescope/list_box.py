# Python imports

# Lib imports
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types



class TelescopeListBoxException(Exception):
    ...



class ListBox(Gtk.ListBox):
    def __init__(self):
        super(ListBox, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_placeholder( Gtk.Label(label = "Buffers...") )
        self.set_selection_mode( Gtk.SelectionMode.BROWSE )
        self.set_vexpand(True)
        self.set_size_request(120, -1)

    def _setup_signals(self):
        self.connect("row-activated", self._row_activated)
        self.connect("row-selected", self._row_selected)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def _row_activated(self, list_box, row = None):
        row  = self.get_selected_row()
        file = row.get_children()[0].file

        event = Event_Factory.create_event(
            "set_active_file",
            buffer = file.buffer
        )

        self.emit(event)


    def _row_selected(self, list_box, row):
        if not row: return

        file = row.get_children()[0].file
        self.set_buffer(file.buffer)

    def set_active_row(self, buffer):
        for row in self.get_children():
            child = row.get_children()[0]
            if not child.file.buffer == buffer: continue
            self.select_row(row)
            break

    def search_changed(self, entry):
        self.search_buffer_names(entry)
        for row in self.get_children():
            if not row.is_visible(): continue
            self.select_row(row)

    def search_buffer_names(self, entry):
        text = entry.get_text()
        if not text:
            for row in self.get_children():
                row.show()

            return

        for row in self.get_children():
            child = row.get_children()[0]

            row.show() \
            if text in child.get_label() else \
            row.hide()

    def activate_row(self):
        self._row_activated(self)

    def set_buffer(self, buffer):
        raise TelescopeListBoxException("ListBox must have 'set_buffer' monkey patched...")

    def move_row_selection_up(self):
        row      = self.get_selected_row()
        next_row = self.get_row_at_index(row.get_index() - 1)

        if not next_row:
            next_row = self.get_row_at_index(
                len( self.get_children() ) - 1
            )

        self.select_row(next_row)

    def move_row_selection_down(self):
        row      = self.get_selected_row()
        next_row = self.get_row_at_index(row.get_index() + 1)

        if not next_row:
            next_row = self.get_row_at_index(0)

        self.select_row(next_row)

    def add_row(self, file):
        label      = Gtk.Label(label = file.fname)
        label.file = file
        label.show()
        self.add(label)

    def remove_row(self, event):
        for row in self.get_children():
            child = row.get_children()[0]
            if not child.file == event.file: continue
            child.file = None
            self.remove(row)
            break

    def update_label(self, event):
        for row in self.get_children():
            child = row.get_children()[0]
            if not child.file == event.file: continue
            child.set_label(event.file.fname)
            break
