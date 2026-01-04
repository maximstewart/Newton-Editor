# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Open File(s) Command")
    gfiles = event_system.emit_and_await("open-files")
    if not gfiles: return

    size   = len(gfiles)
    for i, gfile in enumerate(gfiles):
        file = view.files_manager.new()
        view.command.exec_with_args("load_file", (view, gfile, file))

        if i == (size - 1):
            buffer = view.get_buffer()
            _file  = view.files_manager.get_file(buffer)
            _file.remove_observer(view)

            view.set_buffer(file.buffer)
            file.add_observer(view)
            view.command.exec("update_info_bar")
