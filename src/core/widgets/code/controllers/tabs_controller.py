# Python imports

# Lib imports

# Application imports
from libs.dto.code import (
    CodeEvent,
    FocusedViewEvent,
    FilePathSetEvent,
    RemoveFileEvent,
    SetActiveFileEvent,
    AddedNewFileEvent,
    PoppedFileEvent,
    RemovedFileEvent
)

from ..tabs_widget import TabsWidget
from ..tab_widget import TabWidget

from ..source_view import SourceView

from .controller_base import ControllerBase



class TabsController(ControllerBase):
    def __init__(self):
        super(TabsController, self).__init__()

        self.active_view: SourceView = None
        self.tabs_widget: TabsWidget = TabsWidget()


    def _controller_message(self, event: CodeEvent):
        if isinstance(event, FocusedViewEvent):
            self.active_view = event.view
        elif isinstance(event, FilePathSetEvent):
            self.update_tab_label(event)
        elif isinstance(event, AddedNewFileEvent):
            self.add_tab(event)
        elif isinstance(event, PoppedFileEvent):
            ...
        elif isinstance(event, RemovedFileEvent):
            self.remove_tab(event)
    
    def get_tabs_widget(self):
        return self.tabs_widget

    def update_tab_label(self, event: FilePathSetEvent):
        for tab in self.tabs_widget.get_children():
            if not event.file == tab.file: continue
            tab.label.set_label(event.file.fname)
            break

    def add_tab(self, event: AddedNewFileEvent):
        def set_active_tab(tab, eve, file):
            event        = SetActiveFileEvent()
            event.buffer = tab.get_parent().file.buffer

            self.active_view.set_buffer(
                tab.get_parent().file.buffer
            )

            self.message_all(event)

        def close_tab(tab, eve, file):
            event        = RemoveFileEvent()
            event.buffer = tab.get_parent().file.buffer

            self.message_all(event)

        tab = TabWidget()
        tab.file = event.file
        tab.label.set_label(event.file.fname)
        tab.set_select_signal(set_active_tab)
        tab.set_close_signal(close_tab)

        self.tabs_widget.add(tab)
        tab.show()

    def remove_tab(self, event: RemovedFileEvent):
        for tab in self.tabs_widget.get_children():
            if not event.file == tab.file: continue

            tab.clear_signals_and_data()
            tab.run_dispose()
            tab.destroy()

            del tab
            break
