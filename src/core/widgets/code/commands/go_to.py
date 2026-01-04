# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Go-To Command")

    file    = view.command.exec("get_current_file")
    gfile   = file.get_location()
    uri     = gfile.get_uri()

    buffer  = view.get_buffer()
    iter    = buffer.get_iter_at_mark( buffer.get_insert() )
    line    = iter.get_line()
    offset  = iter.get_line_offset()

    event_system.emit(
        "textDocument/definition",
        (view, file.ftype, uri, line, offset,)
    )
