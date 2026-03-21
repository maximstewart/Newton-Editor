# Python imports

# Lib imports
import gi
from gi.repository import Gtk

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
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        header.set_title("Plugins")
        self.set_titlebar(header)
        header.show()

        window = widget_registery.get_object("main-window")
        self.set_transient_for(window)

    def _setup_signals(self):
        ...

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
            box.destroy()
            break
