# Python imports

# Lib imports
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

# Application imports
from plugins.plugin_types import PluginCode

from libs.event_factory import Event_Factory, Code_Event_Types

from . import create_split_view,    \
              close_split_view,     \
              focus_left_sibling,   \
              focus_right_sibling,  \
              move_to_left_sibling, \
              move_to_right_sibling



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        ...

    def load(self):
        gemit_to = self.emit_to
        self._manage_signals("register_command")

    def unload(self):
        self._manage_signals("unregister_command")

    def _manage_signals(self, action: str):
        _create_split_view         = create_split_view
        _close_split_view          = close_split_view
        _create_split_view.emit_to = self.emit_to
        _close_split_view.emit_to  = self.emit_to

        event = Event_Factory.create_event(action,
            command_name = "create_split_view",
            command      = _create_split_view,
            binding_mode = "released",
            binding      = ["<Control>\\", "<Shift><Control>|"]
        )

        self.emit_to("source_views", event)

        event = Event_Factory.create_event(action,
            command_name = "close_split_view",
            command      = _close_split_view,
            binding_mode = "released",
            binding      = "<Shift><Control>w"
        )

        self.emit_to("source_views", event)

        event = Event_Factory.create_event(action,
            command_name = "focus_left_sibling",
            command      = focus_left_sibling,
            binding_mode = "released",
            binding      = "<Control>Page_Up"
        )

        self.emit_to("source_views", event)

        event = Event_Factory.create_event(action,
            command_name = "focus_right_sibling",
            command      = focus_right_sibling,
            binding_mode = "released",
            binding      = "<Control>Page_Down"
        )

        self.emit_to("source_views", event)

        event = Event_Factory.create_event(action,
            command_name = "move_to_left_sibling",
            command      = move_to_left_sibling,
            binding_mode = "released",
            binding      = "<Control><Shift>Up"
        )

        self.emit_to("source_views", event)

        event = Event_Factory.create_event(action,
            command_name = "move_to_right_sibling",
            command      = move_to_right_sibling,
            binding_mode = "released",
            binding      = "<Control><Shift>Down"
        )

        self.emit_to("source_views", event)

    def run(self):
        ...
