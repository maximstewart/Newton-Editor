# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Get File Type Command")

    buffer = view.get_buffer()
    file   = view.files_manager.get_file(buffer)
    return file.ftype 
