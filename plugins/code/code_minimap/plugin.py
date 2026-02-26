# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .code_minimap import CodeMiniMap



code_minimap = CodeMiniMap()



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.FocusedViewEvent):
            code_minimap.set_smini_view(event.view)

    def load(self):
        editors_container = self.requests_ui_element("editors-container")
        editors_container.add( code_minimap )

    def run(self):
        ...
