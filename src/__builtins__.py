# Python imports
import builtins
import traceback
import threading
import sys

# Lib imports

# Application imports
# from libs.db import DB
from libs.event_system import EventSystem
from libs.keybindings import Keybindings
from libs.logger import Logger
from libs.settings.manager import SettingsManager
from libs.widget_registery import WidgetRegisteryController



# NOTE: Threads WILL NOT die with parent's destruction.
def threaded_wrapper(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target = fn, args = args, kwargs = kwargs, daemon = False)
        thread.start()
        return thread
    return wrapper

# NOTE: Threads WILL die with parent's destruction.
def daemon_threaded_wrapper(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target = fn, args = args, kwargs = kwargs, daemon = True)
        thread.start()
        return thread
    return wrapper

def call_chain_wrapper(fn):
    def wrapper(*args, **kwargs):
        for line in traceback.format_stack():
            print( line.strip() )

        return fn(*args, **kwargs)
    return wrapper


# NOTE: Just reminding myself we can add to builtins two different ways...
# __builtins__.update({"event_system": Builtins()})
builtins.APP_NAME          = "Newton"

builtins.keybindings       = Keybindings()
builtins.event_system      = EventSystem()
builtins.settings_manager  = SettingsManager()
builtins.widget_registery  = WidgetRegisteryController()
# builtins.db                = DB()

settings_manager.load_settings()

builtins.logger            = Logger(
                                settings_manager.path_manager.get_home_config_path(), \
                                _ch_log_lvl = settings_manager.settings.debugging.ch_log_lvl, \
                                _fh_log_lvl = settings_manager.settings.debugging.fh_log_lvl
                            ).get_logger()

builtins.threaded          = threaded_wrapper
builtins.daemon_threaded   = daemon_threaded_wrapper
builtins.call_chain        = call_chain_wrapper



def custom_except_hook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
#
    logger.error("Uncaught exception", exc_info = (exc_type, exc_value, exc_traceback))
#
sys.excepthook = custom_except_hook