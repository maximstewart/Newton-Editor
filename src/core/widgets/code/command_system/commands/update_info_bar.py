# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View,
):
    logger.debug("Command: Update Info Bar")
    file   = view.command.get_file(view)

    if not file: return

    buffer = file.buffer
    iter   = buffer.get_iter_at_mark( buffer.get_insert() )
    line   = iter.get_line() + 1
    column = iter.get_line_offset()
    ftype  = file.ftype.get_id() if hasattr(file.ftype, "get_id") else file.ftype

    event_system.emit(
        "set-info-labels",
        (file.fpath, f"{line}:{column}", ftype, file.encoding)
    )
