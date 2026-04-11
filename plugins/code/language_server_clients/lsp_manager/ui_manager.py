# Python imports
from os import path

# Lib imports
import gi

from gi.repository import GObject
from gi.repository import Gtk

# Application imports
from .mixins.ui_manager_setup_mixin   import UIManagerSetupMixin
from .mixins.ui_manager_events_mixin  import UIManagerEventsMixin
from .mixins.ui_manager_clients_mixin import UIManagerClientsMixin



class UIManager(
    Gtk.Dialog,
    UIManagerSetupMixin,
    UIManagerEventsMixin,
    UIManagerClientsMixin
):
    __gsignals__ = {
        'create-client': (GObject.SignalFlags.RUN_LAST, None, (str, str)),
        'close-client':  (GObject.SignalFlags.RUN_LAST, None, (str,)),
    }

    def __init__(self):
        super(UIManager, self).__init__()
        self._USER_HOME = path.expanduser("~")
        self.client_configs: dict[str, str] = {}
        self.source_view = None

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def map_parent_resize_event(self, parent):
        self.size_allocate_id = parent.connect("size-allocate", lambda w, r: self._map_resize(self, parent))

    def unmap_parent_resize_event(self, parent):
        parent.disconnect(self.size_allocate_id)
