# Python imports

# Lib imports
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

# Application imports



class PluginsUI(Gtk.Dialog):
    def __init__(self):
        super(PluginsUI, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        header   = Gtk.HeaderBar()
        self.ctx = self.get_style_context()
        self.ctx.add_class("plugin-ui")

        self.set_title("Plugins")
        self.set_size_request(450, 530)
        self.set_modal(False)
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        header.set_title("Plugins")
        self.set_titlebar(header)
        header.show()

        window = widget_registery.get_object("main-window")
        self.set_transient_for(window)
        self.set_destroy_with_parent(True)

        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)

    def _setup_signals(self):
        self.connect("focus-out-event", self._on_focus_out)
        self.connect("key-release-event", self._on_key_release)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        widget_registery.expose_object("plugin-ui", self)

        content_area  = self.get_content_area()
        scrolled_win  = Gtk.ScrolledWindow()
        viewport      = Gtk.Viewport()
        self.list_box = Gtk.ListBox()

        self.list_box.set_selection_mode( Gtk.SelectionMode.NONE )
        scrolled_win.set_vexpand(True)

        viewport.add(self.list_box)
        scrolled_win.add(viewport)
        content_area.add(scrolled_win)

        scrolled_win.show_all()

    def _on_key_release(self, widget, event):
        ctrl_pressed  = event.state & Gdk.ModifierType.CONTROL_MASK
        shift_pressed = event.state & Gdk.ModifierType.SHIFT_MASK

        if ctrl_pressed:
            if shift_pressed:
                if event.keyval == Gdk.KEY_P:
                    self.hide()

    def _on_focus_out(self, *args):
        self.hide()
        GLib.idle_add(self.hide)

    def add_row(self, manifest_meta, callback: callable):
        box         = Gtk.Box()
        plugin_lbl  = Gtk.Label(label = manifest_meta.manifest.name)
        author_lbl  = Gtk.Label(label = manifest_meta.manifest.author)
        version_lbl = Gtk.Label(label = manifest_meta.manifest.version)
        is_autoload = manifest_meta.manifest.autoload
        toggle_bttn = Gtk.ToggleButton(label = "Unload" if is_autoload else "Load")

        toggle_bttn.set_active(is_autoload)
        plugin_lbl.set_hexpand(True)
        box.set_hexpand(True)
        version_lbl.set_margin_left(15)
        version_lbl.set_margin_right(15)
        toggle_bttn.set_size_request(120, -1)

        toggle_bttn.toggle_id = \
            toggle_bttn.connect("toggled", callback, manifest_meta)
        box.toggle_bttn = toggle_bttn

        box.add(plugin_lbl)
        box.add(author_lbl)
        box.add(version_lbl)
        box.add(toggle_bttn)
        box.manifest_meta = manifest_meta

        box.show_all()
        self.list_box.add(box)

    def remove_row(self, manifest_meta):
        for row in self.list_box.get_children():
            child = row.get_children()[0]
            if not child.manifest_meta == manifest_meta: continue

            child.manifest_meta = None
            toggle_bttn         = getattr(child, "toggle_bttn", None)
            toggle_bttn.disconnect(toggle_bttn.toggle_id)

            self.list_box.remove(row)
            child.destroy()
            break
