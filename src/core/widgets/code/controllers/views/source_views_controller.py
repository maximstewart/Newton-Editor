# Python imports

# Lib imports

# Application imports
from libs.controllers.controller_base import ControllerBase
from libs.event_factory import Event_Factory, Code_Event_Types

from libs.dto.states import SourceViewStates

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
        elif isinstance(event, Code_Event_Types.RegisterCommandEvent):
            self._register_command(event)

        if not self.signal_mapper.active_view: return

        if isinstance(event, Code_Event_Types.TextChangedEvent):
            self.signal_mapper.active_view.command.exec("update_info_bar")
        elif isinstance(event, Code_Event_Types.SetActiveFileEvent):
            self.signal_mapper.set_buffer_to_active_view(event.buffer)
        elif isinstance(event, Code_Event_Types.TextInsertedEvent):
            self.signal_mapper.insert_text(event.file, event.text)

    def _register_command(self, event: Code_Event_Types.RegisterCommandEvent):
        if not isinstance(event.binding, list):
            event.binding = [ event.binding ]

        for binding in event.binding:
            self.state_manager.key_mapper.map_command(
                event.command_name,
                {
                    f"{event.binding_mode}": binding
                }
            )

        for view in self:
            view.command.add_command(
                event.command_name,
                event.command
            )

    def _get_command_system(self):
        event   = Event_Factory.create_event("get_new_command_system")
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

    def create_source_view(self, state: SourceViewStates = SourceViewStates.INSERT):
        source_view: SourceView = SourceView(state)
        source_view.command     = self._get_command_system()
        source_view.command.set_data(source_view)

        self.signal_mapper.connect_signals(source_view)

        self.append(source_view)
        return source_view

    def first_map_load(self):
        for source_view in self:
            source_view.command.exec("new_file")
            if not source_view.sibling_left: continue
            source_view.get_parent().hide()

        source_view = self[0]
        source_view.grab_focus()
        source_view.command.exec("load_start_files")
