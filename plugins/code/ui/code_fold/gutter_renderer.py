# Python imports

# Lib imports
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GtkSource", "4")

from gi.repository import Gtk
from gi.repository import GtkSource

# Application imports
from .folding_actions import collapse_range, expand_range



def handle_collapse(view, fold):
    collapse_range(view, fold)

def handle_expand(view, fold):
    expand_range(view, fold)

def handle_block_toggle(collapsed, view, fold):
    if not collapsed:
        handle_collapse(view, fold)
    else:
        handle_expand(view, fold)

def is_fold_hidden(buffer, fold):
    iter_ = buffer.get_iter_at_line(fold["start_line"] + 1)
    tags = iter_.get_tags()
    return any(tag.get_property("invisible") for tag in tags)


def on_query_data(renderer, start_iter, end_iter, state, view):
    line = start_iter.get_line()

    if not line in view.fold_start_set:
        renderer.set_text("", -1)
        return

    fold = next(
        (f for f in view.fold_starts if f["start_line"] == line), None
    )

    collapsed = fold and is_fold_hidden(view.get_buffer(), fold)

    renderer.set_text("▶" if collapsed else "▼", -1)

def on_click(view, event, renderer):
    if not event.button == 1:      return False
    window = view.get_window(Gtk.TextWindowType.LEFT)
    if not event.window == window: return False

    x, y = view.window_to_buffer_coords(
        Gtk.TextWindowType.LEFT, int(event.x), int(event.y)
    )

    _, iter_ = view.get_iter_at_location(x, y)
    line     = iter_.get_line()

    if line not in view.fold_start_set: return False

    for fold in view.fold_starts:
        if not fold["start_line"] == line: continue

        collapsed = is_fold_hidden(view.get_buffer(), fold)
        handle_block_toggle(collapsed, view, fold)

        renderer.queue_draw()
        return True

    return False


def setup_gutter(view):
    gutter = view.get_gutter(Gtk.TextWindowType.LEFT)
    buffer = view.get_buffer()

    view.fold_starts    = []
    view.fold_start_set = set()

    renderer = GtkSource.GutterRendererText()
    renderer.set_size(12)
    renderer.set_padding(2, -1)

    renderer.query_data_id = renderer.connect("query-data", on_query_data, view)
    view.collapse_click_id = view.connect("button-press-event", on_click, renderer)

    gutter.insert(renderer, 0)
    view.fold_renderer = renderer
