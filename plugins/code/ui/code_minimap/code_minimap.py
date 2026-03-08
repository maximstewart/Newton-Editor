# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')
from gi.repository.GtkSource import Map
from gi.repository import Pango

# Application imports



class CodeMiniMap(Map):
    def __init__(self):
        super(CodeMiniMap, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("mini-view")

        self.set_hexpand(False)
        self._set_font_desc()

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe(f"set-mini-view", self.set_smini_view)

    def _load_widgets(self):
        ...

    def _set_font_desc(self):
        default_font = 'Monospace 1'
        desc         = Pango.FontDescription(default_font)

        desc.set_size(Pango.SCALE) # Set size to 1pt
        desc.set_family('BuilderBlocks,' + desc.get_family())
        self.set_property('font-desc', desc)

    def set_smini_view(self, source_view):
        self.set_view(source_view)