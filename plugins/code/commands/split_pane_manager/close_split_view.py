# Python imports

# Lib imports
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import Gtk
from gi.repository import GtkSource

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types



emit_to: callable = None

def execute(
    source_view,
    char_str,
    modkeys_states
):
    logger.debug("Command: Close Split Pane")

    scrolled_win = source_view.get_parent()
    pane         = scrolled_win.get_parent()

    if not isinstance(pane, Gtk.Paned): return

    container    = pane.get_parent()
    source_view1 = pane.get_child1()
    source_view2 = pane.get_child2()

    if scrolled_win == source_view1:
        remaining    = source_view2
        closing_view = source_view
    else:
        remaining    = source_view1
        closing_view = source_view

    remaining_view = remaining.get_child()
    left           = closing_view.sibling_left
    right          = closing_view.sibling_right

    if left:
        left.sibling_right = right

    if right:
        right.sibling_left = left

    pane.remove(source_view1)
    pane.remove(source_view2)

    container.remove(pane)
    container.add(remaining)

    event = Event_Factory.create_event(
        "remove_source_view",
        view = closing_view
    )
    emit_to("source_views", event)

    remaining_view.grab_focus()
