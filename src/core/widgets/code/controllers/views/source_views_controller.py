# Python imports

# Lib imports

# Application imports
from libs.controllers.controller_base import ControllerBase
from libs.event_factory import Event_Factory, Code_Event_Types

from ...source_view import SourceView

from .state_manager import SourceViewStateManager
from .signal_mapper import SourceViewSignalMapper



class SourceViewsController(ControllerBase, list):
    def __init__(self):
        super(SourceViewsController, self).__init__()

        self.state_manager: SourceViewStateManager = SourceViewStateManager()
        self.signal_mapper: SourceViewSignalMapper = SourceViewSignalMapper()

        self.signal_mapper.bind_emit(self.emit)
        self.signal_mapper.set_state_manager(self.state_manager)


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.RemovedFileEvent):
            self._remove_file(event)

        if not self.signal_mapper.active_view: return

        if isinstance(event, Code_Event_Types.TextChangedEvent):
            if not self.signal_mapper.active_view: return
            self.signal_mapper.active_view.command.exec("update_info_bar")
        elif isinstance(event, Code_Event_Types.SetActiveFileEvent):
            self.signal_mapper.active_view.set_buffer(
                event.buffer
            )
        elif isinstance(event, Code_Event_Types.TextInsertedEvent):
            self.signal_mapper.insert_text(event.file, event.text)

    def _get_command_system(self):
        event   = Event_Factory.create_event("get_command_system")
        self.message_to("commands", event)
        command = event.response

        del event
        return command

    def _remove_file(self, event: Code_Event_Types.RemovedFileEvent):
        for source_view in self:
            if not event.file.buffer == source_view.get_buffer(): continue
            if not event.next_file:
                source_view.command.exec("new_file")
                continue

            source_view.set_buffer(event.next_file.buffer)

    def create_source_view(self):
        source_view: SourceView = SourceView()
        source_view.command     = self._get_command_system()
        source_view.command.set_data(source_view)

        self.signal_mapper.connect_signals(source_view)

        self.append(source_view)
        return source_view

    def first_map_load(self):
        for source_view in self:
            source_view.command.exec("new_file")

        source_view = self[0]
        source_view.grab_focus()
        source_view.command.exec("load_start_files")
