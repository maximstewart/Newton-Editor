# Python imports

# Lib imports
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import GLib
from gi.repository import Gtk

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types
from plugins.plugin_types import PluginCode

from .fold_types import FOLD_NODES
from .folding_actions import collapse_range
from .folding_engine import get_folding_ranges
from .gutter_renderer import setup_gutter



class Plugin(PluginCode):
    def _controller_message(self, event):
        if isinstance(event, Code_Event_Types.FocusedViewEvent):
            self.view = event.view

            event = Event_Factory.create_event(
                "get_file", buffer=self.view.get_buffer()
            )
            self.emit_to("files", event)

            file = event.response

            if not file: return
            if file.ftype not in FOLD_NODES: return
            if not hasattr(file, "ast"): return

            buffer = file.buffer
            if not buffer.get_tag_table().lookup("invisible"):
                tag = buffer.create_tag("invisible")
                tag.set_property("invisible", True)

            self.update_gutter(file, self.view)
        elif isinstance(event, Code_Event_Types.TextChangedEvent):
            if event.file.ftype not in FOLD_NODES: return
            if not hasattr(event.file, "ast"): return

            self.schedule_update(event.file, self.view)

    def load(self):
        event = Event_Factory.create_event("get_source_views")
        self.emit_to("source_views", event)

        for view in event.response:
            setup_gutter(view)

    def unload(self):
        event = Event_Factory.create_event("get_source_views")
        self.emit_to("source_views", event)

        for view in event.response:
            view.fold_renderer.disconnect(view.fold_renderer.query_data_id)
            view.disconnect(view.collapse_click_id)

            gutter = view.get_gutter(Gtk.TextWindowType.LEFT)
            gutter.remove(view.fold_renderer)

    def run(self):
        ...

    def schedule_update(self, file, view, delay=250):
        if hasattr(view, "fold_update_source") and view.fold_update_source:
            GLib.source_remove(view.fold_update_source)

        def callback():
            self.update_gutter(file, view)

            if hasattr(view, "fold_renderer"):
                view.fold_renderer.queue_draw()

            view.fold_update_source = None
            return False

        view.fold_update_source = GLib.timeout_add(delay, callback)

    def update_gutter(self, file, view):
        view.fold_starts    = get_folding_ranges(file.ftype, file.ast)
        view.fold_start_set = {
            fold["start_line"] for fold in view.fold_starts
        }
