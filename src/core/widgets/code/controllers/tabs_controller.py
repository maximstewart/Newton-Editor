# Python imports

# Lib imports
import gi

from gi.repository import Gtk

# Application imports
from libs.controllers.controller_base import ControllerBase
from libs.event_factory import Event_Factory, Code_Event_Types

from ..tabs_widget import TabsWidget
from ..tab_widget import TabWidget

from ..source_view import SourceView



class TabsController(ControllerBase):
    def __init__(self):
        super(TabsController, self).__init__()

        self.tabs_widget: TabsWidget = TabsWidget()
        self.tabs_widget.message     = self.message


    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.FocusedViewEvent):
            self.tabs_widget.view_changed( event.view.get_buffer() )
        elif isinstance(event, Code_Event_Types.FilePathSetEvent):
            self.update_tab_label(event)
        elif isinstance(event, Code_Event_Types.ModifiedChangedEvent):
            self.tabs_widget.modified_changed( event.buffer )
        elif isinstance(event, Code_Event_Types.FileExternallyDeletedEvent):
            self.tabs_widget.externally_deleted( event.buffer )
        elif isinstance(event, Code_Event_Types.AddedNewFileEvent):
            self.add_tab(event)
        elif isinstance(event, Code_Event_Types.PoppedFileEvent):
            ...
        elif isinstance(event, Code_Event_Types.RemovedFileEvent):
            self.remove_tab(event)
    
    def get_tabs_widget(self):
        return self.tabs_widget

    def update_tab_label(self, event: Code_Event_Types.FilePathSetEvent):
        for page_widget in self.tabs_widget.get_children():
            tab = self.tabs_widget.get_tab_label(page_widget)
            if not event.file == tab.file: continue

            tab.label.set_label(event.file.fname)

            break

    def add_tab(self, event: Code_Event_Types.AddedNewFileEvent):
        tab      = TabWidget()
        tab.file = event.file

        tab.label.set_label(event.file.fname)

        self.tabs_widget.append_page(Gtk.Separator(), tab)
        tab.show_all()

    def remove_tab(self, event: Code_Event_Types.RemovedFileEvent):
        for page_widget in self.tabs_widget.get_children():
            tab = self.tabs_widget.get_tab_label(page_widget)
            if not event.file == tab.file: continue

            tab.clear_signals_and_data()
            self.tabs_widget.remove_page(
                self.tabs_widget.page_num(page_widget)
            )

            break
