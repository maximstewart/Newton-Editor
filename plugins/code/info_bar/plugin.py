# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .info_bar_widget import InfoBarWidget



info_bar_widget = InfoBarWidget()



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.SetInfoLabelsEvent):
            info_bar_widget._set_info_labels(*event.info)

    def load(self):
        header = self.requests_ui_element("header-container")
        header.add( info_bar_widget )

    def run(self):
        ...
