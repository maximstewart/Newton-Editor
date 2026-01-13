# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View,
    language: str
):
    logger.debug("Command: Set Buffer Language")

    buffer = view.get_buffer()
    buffer.set_language(
        view.language_manager.get_language(language)
    )
