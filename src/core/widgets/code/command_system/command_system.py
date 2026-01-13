# Python imports

# Lib imports

# Application imports
from ..event_factory import Event_Factory, Event_Factory_Types
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
        if kwargs:
            return method.execute(*args, kwargs)
        else:
            return method.execute(*args)

    def exec_with_args(self, command: str, args: list) -> any:
        if not hasattr(commands, command): return

        method = getattr(commands, command)
        return method.execute(*args)


    def emit(self, event: Event_Factory_Types.CodeEvent):
        """ Monky patch 'emit' from command controller... """
        ...

    def emit_to(self, controller: str, event: Event_Factory_Types.CodeEvent):
        """ Monky patch 'emit' from command controller... """
        ...


    def get_file(self, view: SourceView):
        event = Event_Factory.create_get_file(
            view   = view,
            buffer = view.get_buffer()
        )

        self.emit_to("files", event)

        return event.response

    def get_swap_file(self, view: SourceView):
        event = Event_Factory.create_get_swap_file(
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
        event = Event_Factory.create_remove_file(
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
