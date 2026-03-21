# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from plugins import plugins_controller

from libs.mixins.ipc_signals_mixin import IPCSignalsMixin
from libs.mixins.keyboard_signals_mixin import KeyboardSignalsMixin

from ..containers.base_container import BaseContainer
from ..containers.code.code_container import CodeContainer

from .base_controller_mixin import BaseControllerMixin
from .bridge_controller import BridgeController



class BaseController(IPCSignalsMixin, KeyboardSignalsMixin, BaseControllerMixin):
    """ docstring for BaseController. """

    def __init__(self):

        self._setup_controller_data()
        self.plugins_controller.manual_launch_plugins()

        self._load_plugins(is_pre = True)
        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_controllers()
        self._load_plugins(is_pre = False)

        logger.info(f"Made it past {self.__class__} loading...")
        settings_manager.set_end_load_time()
        settings_manager.log_load_time()


    def _setup_controller_data(self):
        self.window             = settings_manager.get_main_window()
        self.base_container     = BaseContainer()
        self.plugins_controller = plugins_controller

        settings_manager.register_signals_to_builder([self, self.base_container])

        self._collect_files_dirs()

    def _setup_styling(self):
        ...

    def _setup_signals(self):
        # self.window.connect("focus-out-event", self.unset_keys_and_data)
        # self.window.connect("key-press-event", self.on_global_key_press_controller)
        # self.window.connect("key-release-event", self.on_global_key_release_controller)
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("shutting-down", lambda: print("Shutting down..."))
        event_system.subscribe("handle-file-from-ipc", self.handle_file_from_ipc)
        event_system.subscribe("handle-files-from-ipc", self.handle_files_from_ipc)
        event_system.subscribe("handle-dir-from-ipc", self.handle_dir_from_ipc)
        event_system.subscribe("tggl-top-main-menubar", self._tggl_top_main_menubar)

    def _load_controllers(self):
        BridgeController()

    def _load_plugins(self, is_pre: bool):
        args, unknownargs = settings_manager.get_starting_args()
        if args.no_plugins == "true": return

        if is_pre:
            self.plugins_controller.pre_launch_plugins()
            return

        if not is_pre:
            self.plugins_controller.post_launch_plugins()
            return

    def _tggl_top_main_menubar(self):
        logger.debug("_tggl_top_main_menubar > stub...")
