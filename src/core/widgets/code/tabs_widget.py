# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from .tab_widget import TabWidget



class TabsWidget(Gtk.Notebook):
    def __init__(self):
        super(TabsWidget, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        self.connect("page-added", self._page_added)
        self.switch_page_id = \
            self.connect_after("switch-page", self._switch_page)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def _page_added(self, notebook, page_widget, page_num):
        tab = self.get_tab_label(page_widget)
        tab.set_close_signal(self._close_tab)

        page_widget.show()
        self.set_tab_detachable(page_widget, True)
        self.set_tab_reorderable(page_widget, True)

    def _close_tab(self, tab, eve, file):
        event = Event_Factory.create_event(
            "remove_file",
            buffer = tab.get_parent().file.buffer
        )

        self.message(event)

    def _switch_page(self, notebook, page_widget, page_num):
        tab   = self.get_tab_label(page_widget)
        event = Event_Factory.create_event(
            "set_active_file",
            buffer = tab.file.buffer
        )

        self.message(event)

    def view_changed(self, buffer):
        for page_widget in self.get_children():
            tab = self.get_tab_label(page_widget)
            if not buffer == tab.file.buffer: continue

            self.handler_block(self.switch_page_id)

            self.set_current_page(
                self.page_num(page_widget)
            )

            self.handler_unblock(self.switch_page_id)
