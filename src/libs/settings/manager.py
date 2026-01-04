# Python imports
import inspect
import time

# Lib imports

# Application imports
from ..singleton import Singleton
from .start_check_mixin import StartCheckMixin

from .path_manager import PathManager
from .options.settings import Settings



class SettingsManager(StartCheckMixin, Singleton):
    def __init__(self):
        self.path_manager: PathManager = PathManager()
        self.settings: Settings        = None

        self._main_window              = None
        self._builder                  = None

        self._trace_debug: bool        = False
        self._debug: bool              = False
        self._dirty_start: bool        = False
        self._passed_in_file: bool     = False
        self._starting_files: list     = []

        self.PAINT_BG_COLOR: tuple     = (0, 0, 0, 0.0)

        self.load_keybindings()
        self.load_context_menu_data()


    def get_monitor_data(self) -> list:
        screen = self._main_window.get_screen()
        monitors = []
        for m in range(screen.get_n_monitors()):
            monitors.append(screen.get_monitor_geometry(m))
            print("{}x{}+{}+{}".format(monitor.width, monitor.height, monitor.x, monitor.y))

        return monitors

    def get_main_window(self)        -> any: return self._main_window
    def get_builder(self)            -> any: return self._builder
    def get_paint_bg_color(self)     -> any: return self.PAINT_BG_COLOR
    def get_context_menu_data(self)  -> str: return self._context_menu_data

    def get_icon_theme(self)       -> str:   return self._ICON_THEME
    def get_starting_files(self)   -> list:  return self._starting_files
    def get_guake_key(self)        -> tuple: return self._guake_key

    def get_starting_args(self):
        return self.args, self.unknownargs

    def set_main_window(self, window): self._main_window  = window
    def set_builder(self, builder) -> any:  self._builder = builder

    def set_main_window_x(self, x: int = 0):                 self.settings.config.main_window_x  = x
    def set_main_window_y(self, y: int = 0):                 self.settings.config.main_window_y  = y
    def set_main_window_width(self, width: int = 800):       self.settings.config.main_window_width  = width
    def set_main_window_height(self, height: int = 600):     self.settings.config.main_window_height = height
    def set_main_window_min_width(self, width: int = 720):   self.settings.config.main_window_min_width  = width
    def set_main_window_min_height(self, height: int = 480): self.settings.config.main_window_min_height = height
    def set_starting_files(self, files: list):               self._starting_files = files
    def set_start_load_time(self): self._start_load_time = time.perf_counter()
    def set_end_load_time(self):   self._end_load_time   = time.perf_counter()

    def set_starting_args(self, args, unknownargs):
        self.args = args
        self.unknownargs = unknownargs

    def set_trace_debug(self, trace_debug: bool):
        self._trace_debug = trace_debug

    def set_debug(self, debug: bool):
        self._debug = debug

    def set_is_starting_with_file(self, is_passed_in_file: bool = False):
        self._passed_in_file = is_passed_in_file

    def is_trace_debug(self)       -> str:   return self._trace_debug
    def is_debug(self)             -> str:   return self._debug
    def is_starting_with_file(self) -> bool: return self._passed_in_file

    def log_load_time(self):       logger.info( f"Load Time: {self._end_load_time - self._start_load_time}" )


    def register_signals_to_builder(self, classes = None):
        handlers = {}

        for c in classes:
            methods = None
            try:
                methods = inspect.getmembers(c, predicate = inspect.ismethod)
                handlers.update(methods)
            except Exception as e:
                ...

        self._builder.connect_signals(handlers)

    def call_method(self, target_class: any = None, _method_name: str = "", data: any = None):
        method_name = str(_method_name)
        method      = getattr(target_class, method_name, lambda data: f"No valid key passed...\nkey={method_name}\nargs={data}")
        return method(data) if data else method()

    def load_keybindings(self):
        bindings = self.path_manager.load_keybindings()
        self._guake_key = bindings["guake_key"]

        keybindings.configure(bindings)

    def load_context_menu_data(self):
        self._context_menu_data = self.path_manager.load_context_menu_data()

    def load_settings(self):
        data = self.path_manager.load_settings()
        if not data:
            self.settings = Settings()
            return

        self.settings = Settings(**data)

    def save_settings(self):
        self.path_manager.save_settings(self.settings)
