# Python imports
import json

# Lib imports
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

# Application imports



def add_prettify_json(buffer, menu):
    def on_prettify_json(menuitem, buffer):
        start_itr, \
        end_itr = buffer.get_start_iter(), buffer.get_end_iter()
        data    = buffer.get_text(start_itr, end_itr, False)
        text    = json.dumps(json.loads(data), separators = (',', ':'), indent = 4)

        buffer.begin_user_action()
        buffer.delete(start_itr, end_itr)
        buffer.insert(start_itr, text)
        buffer.end_user_action()

    item = Gtk.MenuItem(label = "Prettify JSON")
    item.connect("activate", on_prettify_json, buffer)
    menu.append(item)