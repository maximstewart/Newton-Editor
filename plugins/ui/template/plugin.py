# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from libs.dto.base_event import BaseEvent

from plugins.plugin_types import PluginUI



class Plugin(PluginUI):
    def __init__(self):
        super(Plugin, self).__init__()


    def _controller_message(self, event: BaseEvent):
        ...

    def load(self):
        ui_element = self.request_ui_element("header-container")
        ui_element.add( self.generate_plugin_element() )

    def run(self):
        ...
 
    def generate_plugin_element(self):
        button = Gtk.Button(label = "Hello, World!")

        button.connect("button-release-event", self.send_message)
        button.show()

        return button

    def send_message(self, widget = None, eve = None):
        logger.info("Hello, World!")
 