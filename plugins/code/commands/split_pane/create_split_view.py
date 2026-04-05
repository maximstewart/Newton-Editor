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

    def _show(pane, alloc, is_vertical: bool):
        if is_vertical:
            pane.set_position(alloc.width  / 2)
        else:
            pane.set_position(alloc.height / 2)

        pane.disconnect(pane.show_id)

    is_control, is_shift, is_alt = modkeys_states
    alloc = container.get_allocation()
    if char_str == "|":
        pane.show_id = pane.connect("show", _show, alloc, True)
        pane.set_orientation(Gtk.Orientation.VERTICAL)
    elif char_str == "\\":
        pane.show_id = pane.connect("show", _show, alloc, False)
        pane.set_orientation(Gtk.Orientation.HORIZONTAL)

    pane.show_all()

    source_view2.command.exec("new_file")
    source_view2.grab_focus()
