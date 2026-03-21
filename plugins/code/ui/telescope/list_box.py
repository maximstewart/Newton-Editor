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
        if not row: return
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
            break

    def fuzzy_score(self, query, text):
        query = query.lower()
        text  = text.lower()
        score = 0
        q_idx = 0

        for char in text:
            if q_idx < len(query) and char == query[q_idx]:
                score += 1
                q_idx += 1

        return score if q_idx == len(query) else 0


    def search_buffer_names(self, entry):
        query = entry.get_text().lower()
        rows  = []

        for row in self.get_children():
            child            = row.get_children()[0]
            label_text       = child.get_label()
            score            = self.fuzzy_score(query, label_text) if query else 1
            child.label_text = label_text if not hasattr(child, "label_text") else child.label_text

            rows.append((score, row, child, label_text))

        rows.sort(key = lambda x: x[0], reverse = True)
        for score, row, child, label_text in rows:
            if query and score > 0:
                highlighted = self.highlight_match(label_text, query)
                child.set_markup(highlighted)
                row.show()
            elif not query:
                child.set_label(child.label_text)
                row.show()
            else:
                row.hide()

    def highlight_match(self, text, query):
        i      = 0
        result = ""

        for char in text:
            if i < len(query) and char.lower() == query[i].lower():
                result += f"<b><i><u>{char}</u></i></b>"
                i += 1
            else:
                result += char

        return result

    def activate_row(self):
        self._row_activated(self)

    def set_buffer(self, buffer):
        raise TelescopeListBoxException("ListBox must have 'set_buffer' monkey patched...")

    def move_row_selection_up(self):
        row = self.get_selected_row()
        if not row: return

        rows = [r for r in self.get_children() if r.is_visible()]
        if not rows: return

        try:
            idx = rows.index(row)
        except ValueError:
            return

        next_idx = (idx - 1) % len(rows)
        self.select_row(rows[next_idx])

    def move_row_selection_down(self):
        row = self.get_selected_row()
        if not row: return

        rows = [r for r in self.get_children() if r.is_visible()]
        if not rows: return

        try:
            idx = rows.index(row)
        except ValueError:
            return

        next_idx = (idx + 1) % len(rows)
        self.select_row(rows[next_idx])

    def add_row(self, file):
        row   = Gtk.ListBoxRow()
        label = Gtk.Label(label = file.fname)
        label.file = file

        row.add(label)
        row.show_all()

        self.add(row)

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
