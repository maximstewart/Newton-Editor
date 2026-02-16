# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ...widgets.code.code_base import CodeBase

from ...widgets.separator_widget import Separator
from ...widgets.code.mini_view_widget import MiniViewWidget

from .editors_container import EditorsContainer



class CodeContainer(Gtk.Box):
    def __init__(self):
        super(CodeContainer, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.VERTICAL)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        code_base = CodeBase()

        self.add( self._create_tabs_widgets(code_base) )
        self.add( self._create_editor_widget(code_base) )

    def _create_tabs_widgets(self, code_base: CodeBase):
        # scrolled_window = Gtk.ScrolledWindow()
        # viewport        = Gtk.Viewport()

        # scrolled_window.set_overlay_scrolling(False)

        # viewport.add( code_base.get_tabs_widget() )
        # scrolled_window.add( viewport )

        # return scrolled_window
        return code_base.get_tabs_widget()

    def _create_editor_widget(self, code_base: CodeBase):
        editors_container = Gtk.Box()

        editors_container.add( Separator("separator_left") )
        editors_container.add( EditorsContainer(code_base) )
        editors_container.add( Separator("separator_right") )
        editors_container.add( code_base.get_mini_view_widget() )

        return editors_container
