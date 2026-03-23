# Python imports

# Lib imports
import gi

gi.require_version('GtkSource', '4')

from gi.repository import GtkSource

# Application imports
from libs.dto.states import SourceViewStates



def execute(
    view: GtkSource.View,
    *args,
    **kwargs
):
    logger.debug("Command: Line Down")
    if not view.state == SourceViewStates.INSERT: return

    view.emit("move-lines", True)
