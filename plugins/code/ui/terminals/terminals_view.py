# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk
from gi.repository import Pango

# Application imports
from .vte_widget import VteWidget



class TerminalsView(Gtk.Notebook):
    def __init__(self):
        super(TerminalsView, self).__init__()

        self.code_view = None

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()

        self.show_all()
        self.hide()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("terminals-view")

        self.set_scrollable(True)

    def _setup_signals(self):
        self.connect("show", self._handle_show)
        self.connect("hide", self._handle_hide)
        self.connect("destroy", self._handle_destroy)

    def _load_widgets(self):
        hbox           = Gtk.Box()
        self.add_bttn  = Gtk.Button(label = "✛")
        self.hide_bttn = Gtk.Button(label = "－")
        self.add_bttn.connect("clicked", self._create_terminal)
        self.hide_bttn.connect("clicked", self._hide_view)

        hbox.add(self.add_bttn)
        hbox.add(self.hide_bttn)
        self.set_action_widget(hbox, Gtk.PackType.END)

        self.create_terminal()
        hbox.show_all()

    def _generate_terminal_parts(self):
        label      = Gtk.Label(label = "...")
        vte_widget = VteWidget()

        vte_widget.hide_view       = self.hide
        vte_widget.create_terminal = self.create_terminal
        vte_widget.close_terminal  = self.close_terminal
        vte_widget.prev_terminal   = self.prev_terminal
        vte_widget.next_terminal   = self.next_terminal

        label.set_text( vte_widget.get_home_path() )
        label.set_tooltip_text( vte_widget.get_home_path() )
        label.set_ellipsize(Pango.EllipsizeMode.START)
        label.set_single_line_mode(True)
        label.set_max_width_chars(32)
        label.set_size_request(240, -1)

        vte_widget.bind_label(label)

        return label, vte_widget

    def _handle_show(self, widget):
        i    = widget.get_current_page()
        term = widget.get_nth_page(i)

        GLib.idle_add(term.grab_focus)

    def _handle_hide(self, widget):
        if not self.code_view: return
        GLib.idle_add(self.code_view.grab_focus)

    def _hide_view(self, widget):
        self.hide()

    def _handle_destroy(self, widget):
        widget.disconnect_by_func(widget._handle_show)
        widget.disconnect_by_func(widget._handle_hide)
        widget.disconnect_by_func(widget._handle_destroy)
        self.add_bttn.disconnect_by_func(self._create_terminal)
        self.hide_bttn.disconnect_by_func(self._hide_view)

    def _create_terminal(self, widget):
        self.create_terminal()

    def set_code_view(self, widget):
        self.code_view = widget

    def create_terminal(self):
        label, vte_widget = self._generate_terminal_parts()
        index = self.append_page(vte_widget, label)
        self.set_tab_detachable(vte_widget, True)
        self.set_tab_reorderable(vte_widget, True)

        self.set_current_page(index)
        GLib.idle_add(vte_widget.grab_focus)

        self.show_all()

    def close_terminal(self):
        size = self.get_n_pages()
        if size == 1: return

        i     = self.get_current_page() 
        widget = self.get_nth_page(i)
        self.remove_page(i)
        widget.destroy()

    def prev_terminal(self):
        i    = self.get_current_page() - 1
        size = self.get_n_pages()

        if i < 0:
            self.set_current_page(size - 1)
            return

        self.prev_page()

    def next_terminal(self):
        i    = self.get_current_page() + 1
        size = self.get_n_pages()

        if i == size:
            self.set_current_page(0)
            return

        self.next_page()
