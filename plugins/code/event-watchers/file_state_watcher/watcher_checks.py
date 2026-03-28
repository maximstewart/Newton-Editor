# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types



def ask_yes_no(message):
    dialog = Gtk.MessageDialog(
        parent       = None,
        flags        = 0,
        message_type = Gtk.MessageType.QUESTION,
        buttons      = Gtk.ButtonsType.YES_NO,
        text         = message,
    )
    dialog.set_title("Confirm")

    response = dialog.run()
    dialog.destroy()

    return response == Gtk.ResponseType.YES


def file_is_deleted(file, emit):
    file.was_deleted = True
    event = Event_Factory.create_event(
        "file_externally_deleted",
        file   = file,
        buffer = file.buffer
    )
    emit(event)


def file_is_externally_modified(file, emit):
    event = Event_Factory.create_event(
        "file_externally_modified",
        file   = file,
        buffer = file.buffer
    )
    emit(event)

    if not file.buffer.get_modified():
        file.reload()
        return

    result = ask_yes_no("File has been externally modified. Reload?")
    if not result: return

    file.reload()
