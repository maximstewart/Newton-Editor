# Python imports

# Lib imports
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types
from libs.dto.states import SourceViewStates



emit_to: callable = None

def execute(
    source_view1,
    char_str,
    modkeys_states
):
    logger.debug("Command: Split Pane")

    scrolled_win1  = source_view1.get_parent()
    container      = scrolled_win1.get_parent()
    pane           = Gtk.Paned()
    event          = Event_Factory.create_event(
        "create_source_view",
        state = SourceViewStates.INSERT
    )
    emit_to("source_views", event)

    scrolled_win2,    \
    source_view2      = event.response
    old_sibling_right = None

    if source_view1.sibling_right:
        old_sibling_right = source_view1.sibling_right

    source_view1.sibling_right = source_view2
    if old_sibling_right:
        old_sibling_right.sibling_left = source_view2
        source_view2.sibling_right     = old_sibling_right

    source_view2.sibling_left  = source_view1

    pane.set_hexpand(True)
    pane.set_vexpand(True)
    pane.set_wide_handle(True)

    container.remove(scrolled_win1)
    pane.pack1( scrolled_win1, True, True )
    pane.pack2( scrolled_win2, True, True )
    container.add(pane)

    pane.show_all()

    is_control, is_shift, is_alt = modkeys_states
    if is_control and is_shift:
        pane.set_orientation(Gtk.Orientation.VERTICAL)
    elif is_control:
        pane.set_orientation(Gtk.Orientation.HORIZONTAL)

    source_view2.grab_focus()
    source_view2.command.exec("new_file")
