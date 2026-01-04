# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Save File Command")
    buffer = view.get_buffer()
    file   = view.files_manager.get_file(buffer)

    if file.ftype == "buffer":
        file.save_as()
        language   = view.language_manager \
                         .guess_language(file.fname, None)
        file.ftype = language
        file.buffer.set_language(language)
        return

    file.save()

