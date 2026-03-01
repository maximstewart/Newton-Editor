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
        tabs_controller = TabsController()
        code_container  = self.request_ui_element("code-container")

        self.register_controller("tabs", tabs_controller)

        code_container.add( tabs_controller.tabs_widget )
        code_container.reorder_child(tabs_controller.tabs_widget, 0)

    def run(self):
        ...
