# Python imports

# Lib imports

# Application imports
from ..event_factory import Event_Factory, Event_Factory_Types

from ..source_file import SourceFile
from ..source_buffer import SourceBuffer

from .foundation.controller_base import ControllerBase



class FilesController(ControllerBase, list):
    def __init__(self):
        super(FilesController, self).__init__()


    def _controller_message(self, event: Event_Factory_Types.CodeEvent):
        if isinstance(event, Event_Factory_Types.AddNewFileEvent):
            self.new_file(event)
        elif isinstance(event, Event_Factory_Types.SwapFileEvent):
            self.swap_file(event)
        elif isinstance(event, Event_Factory_Types.PopFileEvent):
            self.pop_file(event)
        elif isinstance(event, Event_Factory_Types.RemoveFileEvent):
            self.remove_file(event)
        elif isinstance(event, Event_Factory_Types.GetFileEvent):
            self.get_file(event)
        elif isinstance(event, Event_Factory_Types.GetSwapFileEvent):
            self.get_swap_file(event)

    def get_file(self, event: Event_Factory_Types.GetFileEvent):
        if not event.buffer: return

        for file in self:
            if not event.buffer == file.buffer: continue

            event.response = file

            return file

    def get_swap_file(self, event: Event_Factory_Types.GetSwapFileEvent):
        if not event.buffer: return

        for i, file in enumerate(self):
            if not event.buffer == file.buffer: continue

            j              = self.next_index(i)
            next_file      = self[j]
            swapped_file   = self[j] if not j == -1 else None

            event.response = [swapped_file, next_file]

            return swapped_file, next_file

    def new_file(self, event: Event_Factory_Types.AddNewFileEvent):
        file           = SourceFile()
        file.emit      = self.emit
        file.emit_to   = self.emit_to

        event.response = file

        eve = Event_Factory.create_event(
            "added_new_file",
            view = event.view,
            file = file
        )
        self.message_all(eve)

        self.append(file)

        return file

    def swap_file(self, event: Event_Factory_Types.GetSwapFileEvent):
        if not event.buffer: return

        for i, file in enumerate(self):
            if not event.buffer == file.buffer: continue

            j              = self.next_index(i)
            next_file      = self[j]
            swapped_file   = self[j] if not j == -1 else None

            event.response = [swapped_file, next_file]

            return swapped_file, next_file

    def pop_file(self, event: Event_Factory_Types.PopFileEvent):
        if not event.buffer: return

        for i, file in enumerate(self):
            if not event.buffer == file.buffer: continue

            j               = self.next_index(i)
            next_file       = self[j] if not j == -1 else None
            popped_file     = self.pop(i)

            event.response  = [popped_file, next_file]

        eve = Event_Factory.create_event(
            "popped_file",
            view      = view,
            file      = popped_file,
            next_file = next_file
        )
        self.message_all(eve)

        return popped_file, next_file

    def remove_file(self, event: Event_Factory_Types.RemoveFileEvent):
        if not event.buffer: return

        for i, file in enumerate(self):
            if not event.buffer == file.buffer: continue

            j                = self.next_index(i)
            next_file        = self[j] if not j == -1 else None

            event.response   = next_file

            eve = Event_Factory.create_event(
                "removed_file",
                view         = event.view,
                ignore_focus = True,
                file         = file,
                next_file    = next_file
            )
            self.message_all(eve)

            self.remove(file)
            file.close()

            return next_file

    def next_index(self, i):
        size = len(self)

        if (i == 0) & (size >= 2):
            j = i + 1
        elif (i == (size - 1)) & (size >= 2):
            j = i - 1
        elif (size - 1) == 0:
            j = -1
        else:
            j = i + 1

        return j
