# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types



def file_is_deleted(event):
    event.file.was_deleted = True
    event = Event_Factory.create_event(
        "file_externally_deleted",
        file   = event.file,
        buffer = event.buffer
    )
    self.emit(event)


def file_is_externally_modified(event):
#    event = Event_Factory.create_event(
#        "file_externally_modified",
#        file   = event.file,
#        buffer = event.buffer
#    )
#    self.emit(event)

    ...

