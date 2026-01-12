# Python imports

# Lib imports

# Application imports
from libs.dto.code import (
    CodeEvent,
    GetCommandSystemEvent,
    CursorMovedEvent,
    TextChangedEvent,
    FocusedViewEvent,
    SetActiveFileEvent,
    RemoveFileEvent,
    RemovedFileEvent
)

from ..command_system import CommandSystem
from ..key_mapper import KeyMapper

from ..source_view import SourceView

from .controller_base import ControllerBase



class SourceViewsController(ControllerBase, list):
    def __init__(self):
        super(SourceViewsController, self).__init__()

        self.key_mapper: KeyMapper   = KeyMapper()
        self.active_view: SourceView = None


    def get_command_system(self):
        event = GetCommandSystemEvent()
        self.message_to("commands", event)
        command = event.response

        del event
        return command

    def create_source_view(self):
        source_view: SourceView = SourceView()
        source_view.command     = self.get_command_system()
        source_view.command.set_data(source_view)

        self._map_signals(source_view)

        self.append(source_view)
        return source_view

    def _controller_message(self, event: CodeEvent):
        if isinstance(event, RemovedFileEvent):
            self._remove_file(event)
        if isinstance(event, TextChangedEvent):
            self.active_view.command.exec("update_info_bar")

    def _map_signals(self, source_view: SourceView):
        source_view.connect("focus-in-event",       self._focus_in_event)
        source_view.connect("move-cursor",          self._move_cursor)
        source_view.connect("key-press-event",      self._key_press_event)
        source_view.connect("key-release-event",    self._key_release_event)
        source_view.connect("button-press-event",   self._button_press_event)
        source_view.connect("button-release-event", self._button_release_event)

    def _focus_in_event(self, view, eve):
        self.active_view = view

        view.command.exec("set_miniview")
        view.command.exec("set_focus_border")
        view.command.exec("update_info_bar")

        event        = FocusedViewEvent()
        event.view   = view
        self.emit(event)

    def _move_cursor(self, view, step, count, extend_selection):
        event        = CursorMovedEvent()
        buffer       = view.get_buffer()
        iter         = buffer.get_iter_at_mark( buffer.get_insert() )
        line         = iter.get_line()
        char         = iter.get_line_offset()

        event.view   = view
        event.buffer = buffer 
        event.line   = line
        event.char   = char

        self.emit(event)

        view.command.exec("update_info_bar")

    def _button_press_event(self, view, eve):
        self.active_view.command.exec("update_info_bar")

    def _button_release_event(self, view, eve):
        self.active_view.command.exec("update_info_bar")

    def _key_press_event(self, view, eve):
        command = self.key_mapper._key_press_event(eve)
        if not command: return False

        view.command.exec(command)

        return False

    def _key_release_event(self, view, eve):
        command = self.key_mapper._key_release_event(eve)
        if not command: return False

        view.command.exec(command)

        return False

    def _remove_file(self, event: RemovedFileEvent):
        for view in self:
            if not event.file.buffer == view.get_buffer(): continue
            if not event.next_file:
                view.command.exec("new_file")
                continue

            view.set_buffer(event.next_file.buffer)

    def first_map_load(self):
        for view in self:
            view.command.exec("new_file")

        view = self[0]
        view.grab_focus()
        view.command.exec("load_start_files")

