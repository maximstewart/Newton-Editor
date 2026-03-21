# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

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

        self.show()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        self.connect("page-added", self._page_added)
        self.switch_page_id = \
            self.connect_after("switch-page", self._switch_page)
        self.connect("destroy", self._handle_destroy)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def _page_added(self, notebook, page_widget, page_num):
        tab = self.get_tab_label(page_widget)
        tab.set_close_signal(self._close_tab)

        self._bind_tab_menu(tab, page_widget)

        page_widget.show()
        self.set_tab_detachable(page_widget, True)
        self.set_tab_reorderable(page_widget, True)

    def _close_tab(self, button, file):
        event = Event_Factory.create_event(
            "remove_file",
            buffer = file.buffer
        )

        self.emit(event)

    def _switch_page(self, notebook, page_widget, page_num):
        tab   = self.get_tab_label(page_widget)
        event = Event_Factory.create_event(
            "set_active_file",
            buffer = tab.file.buffer
        )

        self.emit(event)
        self._scroll_to_center(tab)

    def _bind_tab_menu(self, tab, page_widget):
        def do_context_menu(tab, eve, page_widget):
            if eve.type == Gdk.EventType.BUTTON_RELEASE and eve.button == 3: # r-click
                menu = self.create_menu(page_widget)
                menu.popup_at_pointer(eve)

        tab._eve_handler_id = \
            tab.event_box.connect(
                "button-release-event",
                do_context_menu,
                page_widget
            )

    def _scroll_to_center(self, tab):
        scrolled_win = self.get_parent().get_parent()
        alloc        = tab.get_allocation()
        tab_x        = alloc.x
        tab_width    = alloc.width
        view_width   = scrolled_win.get_allocated_width()
        target       = tab_x + tab_width / 2 - view_width / 2
        adj          = scrolled_win.get_hadjustment()
        lower        = adj.get_lower()
        upper        = adj.get_upper()
        page_size    = adj.get_page_size()
        target       = max(lower, min(target, upper - page_size))

        adj.set_value(target)

    def create_menu(self, page_widget) -> Gtk.Menu:
        context_menu  = Gtk.Menu()
        close_submenu = Gtk.Menu()
        save_item     = Gtk.MenuItem(label = "Save")
        save_as_item  = Gtk.MenuItem(label = "Save As")

        close_actions_menu = Gtk.MenuItem(label = "Close Actions")
        close_item         = Gtk.MenuItem(label = "Close Tab")
        close_left_item    = Gtk.MenuItem(label = "Close Tabs Left")
        close_right_item   = Gtk.MenuItem(label = "Close Tabs Right")
        close_other_item   = Gtk.MenuItem(label = "Close Other Tabs")
        close_all_item     = Gtk.MenuItem(label = "Close All Tabs")

        save_item.connect("activate",    self.save_item, page_widget)
        save_as_item.connect("activate", self.save_as_item, page_widget)

        close_item.connect("activate",       self.close_item, page_widget)
        close_left_item.connect("activate",  self.close_left_items, page_widget)
        close_right_item.connect("activate", self.close_right_items, page_widget)
        close_other_item.connect("activate", self.close_other_items, page_widget)
        close_all_item.connect("activate",   self.close_all_items, page_widget)

        close_submenu.append(close_item)
        close_submenu.append(close_left_item)
        close_submenu.append(close_right_item)
        close_submenu.append(close_other_item)
        close_submenu.append(close_all_item)

        close_actions_menu.set_submenu(close_submenu)

        context_menu.append(save_item)
        context_menu.append(save_as_item)
        context_menu.append(close_actions_menu)

        context_menu.show_all()

        return context_menu

    def view_changed(self, buffer):
        for page_widget in self.get_children():
            tab = self.get_tab_label(page_widget)
            if not buffer == tab.file.buffer: continue

            self.handler_block(self.switch_page_id)

            self.set_current_page(
                self.page_num(page_widget)
            )
            self.handler_unblock(self.switch_page_id)
            self._scroll_to_center(tab)

            break

    def modified_changed(self, buffer):
        for page_widget in self.get_children():
            tab = self.get_tab_label(page_widget)
            if not buffer == tab.file.buffer: continue

            ctx = tab.label.get_style_context()
            ctx.remove_class("file-deleted")
            if buffer.get_modified():
                ctx.add_class("file-changed")
            else:
                ctx.remove_class("file-changed")

            break

    def externally_deleted(self, buffer):
        for page_widget in self.get_children():
            tab = self.get_tab_label(page_widget)
            if not buffer == tab.file.buffer: continue
            ctx = tab.label.get_style_context()
            ctx.add_class("file-deleted")
            break


    def save_item(self, menu_item, page_widget):
        tab = self.get_tab_label(page_widget)
        tab.file.save()

    def save_as_item(self, menu_item, page_widget):
        tab = self.get_tab_label(page_widget)
        tab.file.save_as()

    def close_item(self, menu_item, page_widget):
        tab = self.get_tab_label(page_widget)
        tab.close_bttn.clicked()

    def close_left_items(self, menu_item, page_widget):
        children = self.get_children()
        i        = children.index(page_widget)

        if i == 0: return

        for widget in children[ : i]:
            tab = self.get_tab_label(widget)
            tab.close_bttn.clicked()

    def close_right_items(self, menu_item, page_widget):
        children = self.get_children()
        i        = children.index(page_widget) + 1

        if i == len(children): return

        for widget in children[i : ]:
            tab = self.get_tab_label(widget)
            tab.close_bttn.clicked()

    def close_other_items(self, menu_item, page_widget):
        self.close_left_items(menu_item, page_widget)
        self.close_right_items(menu_item, page_widget)

    def close_all_items(self, menu_item, page_widget):
        children = self.get_children()

        for widget in children[ : ]:
            tab = self.get_tab_label(widget)
            tab.close_bttn.clicked()

    def _handle_destroy(self, widget):
        self.disconnect_by_func(self._page_added)
        self.disconnect_by_func(self._switch_page)
        self.disconnect_by_func(self._handle_destroy)

