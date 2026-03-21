# Python imports
import json

# Lib imports
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

# Application imports



def on_case_handle(menuitem, buffer, action):
    start_itr, \
    end_itr  = buffer.get_selection_bounds()
    data     = buffer.get_text(start_itr, end_itr, False)
    text     = data

    if action == "on_all_upper":
        text = data.upper()
    elif action == "on_all_lower":
        text = data.lower()
    elif action == "on_invert":
        text = data.swapcase()
    elif action == "on_title":
        text = data.title()
    elif action == "on_title_strip":
        text = data.title().replace("-", "").replace("_", "").replace(" ", "")

    buffer.begin_user_action()
    buffer.delete(start_itr, end_itr)
    buffer.insert(start_itr, text)
    buffer.end_user_action()



def extend_source_view_menu(buffer, menu):
    if not buffer.get_selection_bounds(): return

    for child in menu.get_children():
        if not child.get_label() == "C_hange Case": continue
        menu.remove(child)

    change_case_item = Gtk.MenuItem(label = "Change Case")

    case_menu        = Gtk.Menu()
    au_case_item     = Gtk.MenuItem(label = "All Upper Case")
    al_case_item     = Gtk.MenuItem(label = "All Lower Case")
    inver_case_item  = Gtk.MenuItem(label = "Invert Case")
    title_case_item  = Gtk.MenuItem(label = "Title Case")
    title_strip_case_item = Gtk.MenuItem(label = "Title Strip Case")

    au_case_item.connect("activate",  on_case_handle, buffer, "on_all_upper")
    al_case_item.connect("activate",  on_case_handle, buffer, "on_all_lower")
    inver_case_item.connect("activate", on_case_handle, buffer, "on_invert")
    title_case_item.connect("activate", on_case_handle, buffer, "on_title")
    title_strip_case_item.connect("activate", on_case_handle, buffer, "on_title_strip")

    case_menu.append(au_case_item)
    case_menu.append(al_case_item)
    case_menu.append(inver_case_item)
    case_menu.append(title_case_item)
    case_menu.append(title_strip_case_item)
    change_case_item.set_submenu(case_menu)

    menu.append(change_case_item)
