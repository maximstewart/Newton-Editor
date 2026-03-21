# Python imports

# Lib imports

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

        code_container.add( self.tabs_controller.tabs_widget )
        code_container.reorder_child(self.tabs_controller.tabs_widget, 0)

        event = Event_Factory.create_event("get_files")
        self.emit_to("files", event)
        for file in event.response:
            self.tabs_controller.add_tab(file)

    def unload(self):
        self.unregister_controller("tabs")
        self.tabs_controller.unload_tabs()
        self.tabs_controller.tabs_widget.destroy()

        self.tabs_controller.tabs_widget = None
        self.tabs_controller             = None
        del self.tabs_controller

    def run(self):
        ...
