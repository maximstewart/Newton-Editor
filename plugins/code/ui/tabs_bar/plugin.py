# Python imports

# Lib imports
import gi

from gi.repository import Gtk

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .tabs_controller import TabsController



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
            ...

    def load(self):
        self.tabs_controller = TabsController()
        code_container  = self.request_ui_element("code-container")

        self.register_controller("tabs", self.tabs_controller)

        scrolled_win = Gtk.ScrolledWindow()
        viewport     = Gtk.Viewport()

        scrolled_win.set_overlay_scrolling(False)
        scrolled_win.set_size_request(-1, 50)

        viewport.add( self.tabs_controller.tabs_widget )
        scrolled_win.add( viewport )
        code_container.add( scrolled_win )
        code_container.reorder_child(scrolled_win, 0)

        viewport.show()
        scrolled_win.show()

        event = Event_Factory.create_event("get_files")
        self.emit_to("files", event)
        for file in event.response:
            self.tabs_controller.add_tab(file)

    def unload(self):
        self.unregister_controller("tabs")
        self.tabs_controller.unload_tabs()

        tabs_widget  = self.tabs_controller.tabs_widget
        viewport     = tabs_widget.get_parent()
        scrolled_win = viewport.get_parent()

        tabs_widget.destroy()
        viewport.destroy()
        scrolled_win.destroy()

        self.tabs_controller.tabs_widget = None
        self.tabs_controller             = None
        del self.tabs_controller

    def run(self):
        ...
