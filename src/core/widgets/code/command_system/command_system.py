# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from ..source_view import SourceView

from . import commands



class CommandSystem:
    def __init__(self):
        super(CommandSystem, self).__init__()

        self.data: list = ()


    def set_data(self, *args, **kwargs):
        self.data = (args, kwargs)

    def exec(self, command: str) -> any:
        if not hasattr(commands, command): return
        method = getattr(commands, command)

        args, kwargs = self.data
        return method.execute(*args, **kwargs)

    def exec_with_args(self, command: str, *args, **kwargs) -> any:
        if not hasattr(commands, command): return

        method = getattr(commands, command)
        return method.execute(*args, **kwargs)

    def add_command(self, command_name: str, command: callable):
        setattr(commands, command_name, command)


    def emit(self, event: Code_Event_Types.CodeEvent):
        """ Monkey patch 'emit' from command controller... """
        ...

    def emit_to(self, controller: str, event: Code_Event_Types.CodeEvent):
        """ Monkey patch 'emit_to' from command controller... """
        ...


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
