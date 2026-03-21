# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from ..source_view import SourceView



class CommandSystemMixin:
    def toggle_plugins_ui(self):
        event = Event_Factory.create_event( "toggle_plugins_ui" )

        self.emit_to("plugins", event)

    def filter_out_loaded_files(self, uris: list[str]):
        event = Event_Factory.create_event(
            "filter_out_loaded_files",
            uris = uris
        )

        self.emit_to("files", event)

        return event.response

    def set_info_labels(self, data: tuple[str]):
        event = Event_Factory.create_event(
            "set_info_labels",
            info = data
        )

        self.emit_to("plugins", event)

    def get_file(self, view: SourceView):
        event = Event_Factory.create_event(
            "get_file",
            view   = view,
            buffer = view.get_buffer()
        )

        self.emit_to("files", event)

        return event.response

    def get_swap_file(self, view: SourceView):
        event = Event_Factory.create_event(
            "get_swap_file",
            view   = view,
            buffer = view.get_buffer()
        )

        self.emit_to("files", event)

        return event.response

    def new_file(self, view: SourceView):
        event = Event_Factory.create_event("add_new_file", view = view)

        self.emit_to("files", event)

        return event.response

    def remove_file(self, view: SourceView):
        event = Event_Factory.create_event(
            "remove_file",
            view   = view,
            buffer = view.get_buffer()
        )

        self.emit_to("files", event)

        return event.response

    def request_completion(self, view: SourceView):
        event = Event_Factory.create_event(
            "request_completion",
            view   = view,
            buffer = view.get_buffer()
        )

        self.emit_to("completion", event)
