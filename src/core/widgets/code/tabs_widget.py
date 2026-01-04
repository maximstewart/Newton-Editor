# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from libs.dto.code_event import CodeEvent

from .view import SourceView
from .source_files_manager import SourceFilesManager
from .source_file import SourceFile

from .tab_widget import TabWidget



class TabsWidget(Gtk.ScrolledWindow):
    def __init__(self):
        super(TabsWidget, self).__init__()

        self.active_view: SourceView = None

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_overlay_scrolling(False)

    def _setup_signals(self):
        event_system.subscribe("register-view-to-tabs-widget", self._register_view_to_tabs_widget)

    def _subscribe_to_events(self):
        self.files_manager: SourceFilesManager = SourceFilesManager()
        self.files_manager.add_observer(self)

    def _load_widgets(self):
        self.viewport = Gtk.Viewport()
        self.tabs     = Gtk.ButtonBox()

        self.tabs.set_layout(Gtk.ButtonBoxStyle.CENTER)

        self.viewport.add(self.tabs)
        self.add(self.viewport)

    def _register_view_to_tabs_widget(self, view: SourceView):
        view.add_observer(self)
        view.set_files_manager(self.files_manager)

    def notification(self, event: CodeEvent):
        match event.etype:
            case "focused_view_change":
                logger.debug("SourceView.focused_view_change")
                self.active_view = event.view
            case "appended_file":
                logger.debug("SourceFilesManager.appended")
                self.add_tab(event)
            case "popped_file":
                logger.debug("SourceFilesManager.pop_file")
            case "removed_file":
                logger.debug("SourceFilesManager.remove_file")
                self.remove_tab(event)
            case "set_path":
                logger.debug("SourceFile.set_path")
                self.update_tab_label(event)
            case _:
                ...

    def add_tab(self, event: CodeEvent):
        tab      = TabWidget()
        tab.file = event.file

        tab.label.set_label(event.file.fname)
        event.file.add_observer(self)

        def select_signal(widget, eve, file):
            self.active_view.command.exec_with_args("set_buffer", (self.active_view, file))

        def close_signal(widget, eve, file):
            self.files_manager.remove_file(file.buffer)

        tab.set_select_signal(select_signal)
        tab.set_close_signal(close_signal)

        self.tabs.add(tab)

    def remove_tab(self, event: CodeEvent):
        for child in self.tabs.get_children():
            if not child.file == event.file: continue

            child.file.remove_observer(self)
            self.tabs.remove(child)
            child.clear_signals_and_data()
            del child

            return
    
    def update_tab_label(self, event: CodeEvent):
        for tab in self.tabs.get_children():
            if not tab.file == event.file: continue
            tab.label.set_label(event.file.fname)

            return
