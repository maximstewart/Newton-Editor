# Python imports

# Lib imports
from gi.repository import GtkSource

# Application imports



def set_language_and_style(view, file):
    language   = view.language_manager.guess_language(file.fname, None)
    file.buffer.set_language(language)
    file.buffer.set_style_scheme(view.syntax_theme)

    return language

def update_info_bar_if_focused(command_system, view: GtkSource):
    has_focus = command_system.exec("has_focus")
    if has_focus:
        command_system.exec("update_info_bar")

def get_file_and_buffer(view: GtkSource):
    file   = view.command.get_file(view)
    buffer = file.buffer

    return file, buffer