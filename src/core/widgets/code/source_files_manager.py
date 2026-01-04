# Python imports

# Lib imports

# Application imports
from libs.mixins.observable_mixin import ObservableMixin
from libs.singleton import Singleton
from libs.dto.code_event import CodeEvent

from .source_file import SourceFile
from .source_buffer import SourceBuffer



class SourceFilesManager(Singleton, list, ObservableMixin):
    def __init__(self):
        super(SourceFilesManager, self).__init__()

        self.observers = []


    def new(self):
        file = SourceFile()
        self.append(file)
        return file

    def append(self, file: SourceFile):
        if not file: return
        super().append(file)

        event       = CodeEvent()
        event.etype = "appended_file"
        event.file  = file

        self.notify_observers(event)

    def get_file(self, buffer: SourceBuffer):
        if not buffer: return

        for file in self:
            if not buffer == file.buffer: continue
            return file

    def pop_file(self, buffer: SourceBuffer):
        if not buffer: return

        for i, file in enumerate(self):
            if not buffer == file.buffer: continue

            j               = self.next_index(i)
            next_file       = self[j] if not j == -1 else None
            popped_file     = self.pop(i)
            event           = CodeEvent()
            event.etype     = "popped_file"
            event.file      = popped_file
            event.next_file = next_file

            self.notify_observers(event)

            return popped_file, next_file

    def swap_file(self, buffer: SourceBuffer):
        if not buffer: return

        for i, file in enumerate(self):
            if not buffer == file.buffer: continue

            j            = self.next_index(i)
            next_file    = self[j]
            swapped_file = self[j] if not j == -1 else None

            return swapped_file, next_file

    def remove_file(self, buffer: SourceBuffer):
        if not buffer: return

        for i, file in enumerate(self):
            if not buffer == file.buffer: continue

            j                  = self.next_index(i)
            next_file          = self[j] if not j == -1 else None
            event              = CodeEvent()
            event.etype        = "removed_file"
            event.ignore_focus = True
            event.file         = file
            event.next_file    = next_file
            self.notify_observers(event)

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