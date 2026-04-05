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
        editors_container = self.request_ui_element("editors-container")
        editors_container.add( code_minimap )

        event = Event_Factory.create_event("get_active_view")
        self.emit_to("source_views", event)
        if not event.response: return
        code_minimap.set_smini_view(event.response)

    def unload(self):
        code_minimap.destroy()

    def run(self):
        ...
