# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.info("Save File As Command")
    buffer = view.get_buffer()
    file   = view.files_manager.get_file(buffer)

    file.save_as()

    language   = view.language_manager \
                       .guess_language(file.fname, None)
    file.ftype = language
    file.buffer.set_language(language)
    file.add_observer(view)
    view.exec_command("update_info_bar")
