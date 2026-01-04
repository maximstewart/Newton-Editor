# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GtkSource

# Application imports
from libs.mixins.observable_mixin import ObservableMixin

from .mixins.source_view_events_mixin import SourceViewEventsMixin
from .mixins.source_view_dnd_mixin import SourceViewDnDMixin

from .source_files_manager import SourceFilesManager
from .completion_manager import CompletionManager
from .command_system import CommandSystem
from .key_mapper import KeyMapper



class SourceView(GtkSource.View, ObservableMixin, SourceViewEventsMixin, SourceViewDnDMixin):
    def __init__(self):
        super(SourceView, self).__init__()

        self.observers            = []
        self._cut_temp_timeout_id = None
        self._cut_buffer          = ""

        self.sibling_right = None
        self.sibling_left  = None

        self._setup_styles()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styles(self):
        self.zoom_level = settings_manager.settings.theming.default_zoom
        ctx             = self.get_style_context()

        ctx.add_class("source-view")
        ctx.add_class(f"px{self.zoom_level}")

        self.set_vexpand(True)
        self.set_bottom_margin(800)

        self.set_show_line_marks(True)
        self.set_show_line_numbers(True)
        self.set_smart_backspace(True)
        self.set_indent_on_tab(True)
        self.set_insert_spaces_instead_of_tabs(True)
        self.set_auto_indent(True)
        self.set_monospace(True)
        self.set_tab_width(4)
        self.set_show_right_margin(True)
        self.set_right_margin_position(80)
        self.set_background_pattern(0) # 0 = None, 1 = Grid
        self.set_highlight_current_line(True)

    def _setup_signals(self):
        self.map_id =  self.connect("map", self._init_map)

        self.connect("focus-in-event", self._focus_in_event)
        self.connect("drag-data-received", self._on_drag_data_received)
        self.connect("move-cursor", self._move_cursor)
        self.connect("key-press-event", self._key_press_event)
        self.connect("key-release-event", self._key_release_event)
        self.connect("button-press-event", self._button_press_event)
        self.connect("button-release-event", self._button_release_event)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        self._set_up_dnd()
        event_system.emit("register-view-to-tabs-widget", (self,))

    def _init_map(self, view):
        self.disconnect(self.map_id)
        del self.map_id

        GLib.idle_add(self._init_show)

    def _init_show(self):
        self.language_manager     = GtkSource.LanguageManager()
        self.style_scheme_manager = GtkSource.StyleSchemeManager()

        self.key_mapper           = KeyMapper()
        self.command              = CommandSystem()
        self.completion           = CompletionManager()

        self.command.set_data(self)
        self.completion.set_completer( self.get_completion() )

        self.style_scheme_manager.append_search_path(
            f"{settings_manager.path_manager.get_home_config_path()}/code_styles"
        )
        self.syntax_theme = self.style_scheme_manager.get_scheme(
            f"{settings_manager.settings.theming.syntax_theme}"
        )

        self.command.exec("new_file")

        if not self.sibling_right: return

        self.grab_focus()
        self.command.exec("load_start_files")

        return False

    def set_files_manager(self, files_manager: SourceFilesManager):
        self.files_manager = files_manager
        self.files_manager.add_observer(self)

    def clear_temp_cut_buffer_delayed(self):
        if self._cut_temp_timeout_id:
            GLib.source_remove(self._cut_temp_timeout_id)

    def set_temp_cut_buffer_delayed(self):
        def clear_temp_buffer():
            self._cut_buffer          = ""
            self._cut_temp_timeout_id = None
            return False

        self._cut_temp_timeout_id = GLib.timeout_add(15000, clear_temp_buffer)
