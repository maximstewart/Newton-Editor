# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .controllers.controller_base import ControllerBase
from .dto.base_event import BaseEvent



class WidgetRegisteryController(ControllerBase):
    """docstring for WidgetRegisteryController."""

    def __init__(self):
        super(WidgetRegisteryController, self).__init__()

        self._builder: Gtk.Builder = None
        self.objects: dict         = {}
        self.builder_keys: list    = []

        self._load_glade_file()


    def _load_glade_file(self):
        self._builder = Gtk.Builder.new_from_file( settings_manager.path_manager.get_glade_file() )
        settings_manager.set_builder(self._builder)

        widgets = self._builder.get_objects()
        for widget in widgets:
            self.builder_keys.append( widget.get_name() )

    def _controller_message(self, event: BaseEvent):
        ...

    def list_objects(self, id: str) -> list:
        return self.objects.keys() + self.builder_keys

    def list_non_builder_objects(self, id: str) -> list:
        return self.objects.keys()

    def list_builder_objects(self, id: str) -> list:
        return self.builder_keys

    def get_object(self, id: str) -> any:
        if id in self.objects:
            return self.objects[id]

        return self._builder.get_object(id)

    def expose_object(self, id: str, object: any, use_gtk: bool = False):
        if not use_gtk:
            self.objects[id] = object
            return

        self._builder.expose_object(id, object)
        self.builder_keys.append(id)

    def dereference_object(self, id: str):
        self.builder_keys.remove(id)
        if id in self.objects:
            del self.objects[id]
