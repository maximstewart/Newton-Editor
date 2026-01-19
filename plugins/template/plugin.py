# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from plugins.plugin_base import PluginBase



class Plugin(PluginBase):
    def __init__(self):
        super().__init__()


    def load(self):
        ui_element = self.requests_ui_element("plugin_control_list")
        ui_element.add( self.generate_plugin_element() )

    def run(self):
        ...
 
    def generate_plugin_element(self):
        button = Gtk.Button(label = self.name)

        button.connect("button-release-event", self.send_message)
        button.show()

        return button

    def send_message(self, widget = None, eve = None):
        message = "Hello, World!"
        self.emit("display_message", ("warning", message, None))
 