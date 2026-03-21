# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types



def execute(
    view: GtkSource.View,
    *args,
    **kwargs
):
    logger.debug("Command: Toggle Plugins UI")
    view.command.toggle_plugins_ui()
