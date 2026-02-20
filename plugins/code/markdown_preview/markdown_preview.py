# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk

# Application imports
from core.widgets.webkit.webkit_ui import WebkitUI

from .mixins.markdown_preview_mixin import MarkdownPreviewMixin



class MarkdownPreview(Gtk.Popover, MarkdownPreviewMixin):
    def __init__(self):
        super(MarkdownPreview, self).__init__()

        self.can_hide: bool          = True
        self.is_preview_paused: bool = True # True by default b/c started hidden

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("markdown-preview")

        self.set_modal(False)
        self.set_can_focus(False)
        self.set_transitions_enabled(False)
        self.set_size_request(480, 720)
        self.override_background_color(
            Gtk.StateFlags.NORMAL,
            Gdk.RGBA(0, 0, 0, 0.0)
        )
        self.set_constrain_to(
            Gtk.PopoverConstraint.WINDOW
        )

    def _setup_signals(self):
        self.connect("hide", self._handle_hide)
        self.connect("show", self._handle_show)

    def _load_widgets(self):
        box             = Gtk.Box()
        bttn_box        = Gtk.ButtonBox()
        scrolled_win    = Gtk.ScrolledWindow()
        viewport        = Gtk.Viewport()
        self._markdown_view       = WebkitUI()

        self.start_stop_bttn = Gtk.ToggleButton()
        settings_bttn   = Gtk.Button()

        self.start_stop_bttn.set_label("gtk-media-pause")
        self.start_stop_bttn.set_use_stock(True)

        settings_bttn.set_image(
            Gtk.Image.new_from_stock(
                "gtk-justify-fill",  Gtk.IconSize.BUTTON
            )
        )

        self._markdown_view.set_vexpand(True)
        box.set_orientation(Gtk.Orientation.VERTICAL)

        self.start_stop_bttn.connect("clicked", self._tggle_preview_updates)
        settings_bttn.connect("clicked", self._handle_settings)

        bttn_box.pack_end(self.start_stop_bttn, expand = False, fill = False, padding = 1)
        bttn_box.pack_end(settings_bttn, expand = False, fill = False, padding = 1)
        viewport.add(self._markdown_view)
        scrolled_win.add(viewport)
        box.add(bttn_box)
        box.add(scrolled_win)
        self.add(box)

        box.show_all()


    def _handle_hide(self, widget):
        if self.can_hide:
            self.is_preview_paused = True
            return False

        return True

    def _handle_show(self, widget):
        self.can_hide = False
        self.is_preview_paused = self.start_stop_bttn.get_active()

    def _tggle_preview_updates(self, widget):
        self.is_preview_paused = not self.is_preview_paused

    def _handle_settings(self, widget):
        ...
