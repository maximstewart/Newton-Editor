# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports



def execute(
    view: GtkSource.View  = None
):
    logger.debug("Command: Show Completion")
    completer = view.get_completion()
    providers = completer.get_providers()

    if not providers:
        view.command.request_completion(view)
        return

    completer.start(
        providers,
        completer.create_context()
    )
