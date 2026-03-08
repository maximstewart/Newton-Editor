# Python imports

# Lib imports
import gi

from gi.repository import GLib

# Application imports



def clear_temp_cut_buffer_delayed(view: any):
    if not hasattr(view, "_cut_temp_timeout_id"): return
    if not view._cut_temp_timeout_id: return

    GLib.source_remove(view._cut_temp_timeout_id)

def set_temp_cut_buffer_delayed(view: any):
    def clear_temp_buffer(view: any):
        view._cut_buffer          = ""
        view._cut_temp_timeout_id = None
        return False

    view._cut_temp_timeout_id = GLib.timeout_add(15000, clear_temp_buffer, view)
