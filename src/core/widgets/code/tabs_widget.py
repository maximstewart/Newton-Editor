# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from libs.event_factory import Code_Event_Types

from .source_view import SourceView
from .source_file import SourceFile

from .tab_widget import TabWidget



class TabsWidget(Gtk.ButtonBox):
    def __init__(self):
        super(TabsWidget, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_layout(Gtk.ButtonBoxStyle.CENTER)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def add_tab(self, event: Code_Event_Types.CodeEvent):
        """Add a tab widget for the given file event."""
        if not hasattr(self, 'tabs'):
            return
            
        tab      = TabWidget()
        tab.file = event.file

        tab.label.set_label(event.file.fname)

        def select_signal(widget, eve, file):
            self.code_base.active_view.command.exec_with_args(
                "set_buffer",
                (self.code_base.active_view, file)
            )

        def close_signal(widget, eve, file):
            self.code_base.files_controller.remove_file(file.buffer)

        tab.set_select_signal(select_signal)
        tab.set_close_signal(close_signal)

        self.tabs.add(tab)

    def remove_tab(self, event: Code_Event_Types.CodeEvent):
        """Remove a tab widget for the given file event."""
        if not hasattr(self, 'tabs'):
            return
            
        for child in self.tabs.get_children():
            if not child.file == event.file: continue

            self.tabs.remove(child)
            child.clear_signals_and_data()
            del child

            return
    
    def update_tab_label(self, event: Code_Event_Types.CodeEvent):
        """Update tab label for the given file event."""
        if not hasattr(self, 'tabs'):
            return
            
        for tab in self.tabs.get_children():
            if not tab.file == event.file: continue
            tab.label.set_label(event.file.fname)

            return
