# Python imports
import json
import zipfile

from os import path
from os import mkdir

# Lib imports

# Application imports



class MissingConfigError(Exception):
    pass



class PathManager:
    def __init__(self):
        self._SCRIPT_PTH: str        = path.dirname(path.realpath(__file__))
        self._USER_HOME: str         = path.expanduser('~')
        self._HOME_CONFIG_PATH: str  = f"{self._USER_HOME}/.config/{APP_NAME.lower()}"
        self._USR_PATH: str          = f"/usr/share/{APP_NAME.lower()}"
        self._USR_CONFIG_FILE: str   = f"{self._USR_PATH}/settings.json"

        self._CONTEXT_PATH: str      = f"{self._HOME_CONFIG_PATH}/context_path"
        self._PLUGINS_PATH: str      = f"{self._HOME_CONFIG_PATH}/plugins"
        self._DEFAULT_ICONS: str     = f"{self._HOME_CONFIG_PATH}/icons"
        self._CONFIG_FILE: str       = f"{self._HOME_CONFIG_PATH}/settings.json"
        self._GLADE_FILE: str        = f"{self._HOME_CONFIG_PATH}/Main_Window.glade"
        self._CSS_FILE: str          = f"{self._HOME_CONFIG_PATH}/stylesheet.css"
        self._KEY_BINDINGS_FILE: str = f"{self._HOME_CONFIG_PATH}/key-bindings.json"
        self._PID_FILE: str          = f"{self._HOME_CONFIG_PATH}/{APP_NAME.lower()}.pid"
        self._UI_WIDGETS_PATH: str   = f"{self._HOME_CONFIG_PATH}/ui_widgets"
        self._CONTEXT_MENU: str      = f"{self._HOME_CONFIG_PATH}/context_menu.json"
        self._WINDOW_ICON: str       = f"{self._DEFAULT_ICONS}/{APP_NAME.lower()}.png"

        # self._USR_CONFIG_FILE: str   = f"{self._USR_PATH}/settings.json"
        # self._PLUGINS_PATH: str      = f"plugins"
        # self._CONFIG_FILE: str       = f"settings.json"
        # self._GLADE_FILE: str        = f"Main_Window.glade"
        # self._CSS_FILE: str          = f"stylesheet.css"
        # self._KEY_BINDINGS_FILE: str = f"key-bindings.json"
        # self._PID_FILE: str          = f"{APP_NAME.lower()}.pid"
        # self._WINDOW_ICON: str       = f"{APP_NAME.lower()}.png"
        # self._UI_WIDGETS_PATH: str   = f"ui_widgets"
        # self._CONTEXT_MENU: str      = f"context_menu.json"
        # self._DEFAULT_ICONS: str     = f"icons"


        # with zipfile.ZipFile("files.zip", mode="r", allowZip64=True) as zf:
        #     with io.TextIOWrapper(zf.open("text1.txt"), encoding="utf-8") as f:


        if not path.exists(self._HOME_CONFIG_PATH):
            mkdir(self._HOME_CONFIG_PATH)
        if not path.exists(self._PLUGINS_PATH):
            mkdir(self._PLUGINS_PATH)

        if not path.exists(self._DEFAULT_ICONS):
            self._DEFAULT_ICONS = f"{self._USR_PATH}/icons"
            if not path.exists(self._DEFAULT_ICONS):
                raise MissingConfigError("Unable to find the application icons directory.")
        if not path.exists(self._GLADE_FILE):
            self._GLADE_FILE   = f"{self._USR_PATH}/Main_Window.glade"
            if not path.exists(self._GLADE_FILE):
                raise MissingConfigError("Unable to find the application Glade file.")
        if not path.exists(self._KEY_BINDINGS_FILE):
            self._KEY_BINDINGS_FILE = f"{self._USR_PATH}/key-bindings.json"
            if not path.exists(self._KEY_BINDINGS_FILE):
                raise MissingConfigError("Unable to find the application Keybindings file.")
        if not path.exists(self._CSS_FILE):
            self._CSS_FILE     = f"{self._USR_PATH}/stylesheet.css"
            if not path.exists(self._CSS_FILE):
                raise MissingConfigError("Unable to find the application Stylesheet file.")
        if not path.exists(self._WINDOW_ICON):
            self._WINDOW_ICON  = f"{self._USR_PATH}/icons/{APP_NAME.lower()}.png"
            if not path.exists(self._WINDOW_ICON):
                raise MissingConfigError("Unable to find the application icon.")
        if not path.exists(self._UI_WIDGETS_PATH):
            self._UI_WIDGETS_PATH  = f"{self._USR_PATH}/ui_widgets"
        if not path.exists(self._CONTEXT_MENU):
            self._CONTEXT_MENU  = f"{self._USR_PATH}/context_menu.json"


    def get_glade_file(self)       -> str: return self._GLADE_FILE
    def get_ui_widgets_path(self)  -> str: return self._UI_WIDGETS_PATH
    def get_context_path(self)     -> str: return self._CONTEXT_PATH
    def get_plugins_path(self)     -> str: return self._PLUGINS_PATH
    def get_css_file(self)         -> str: return self._CSS_FILE
    def get_home_config_path(self) -> str: return self._HOME_CONFIG_PATH
    def get_window_icon(self)      -> str: return self._WINDOW_ICON
    def get_home_path(self)        -> str: return self._USER_HOME

    def load_keybindings(self):
        try:
            with open(self._KEY_BINDINGS_FILE) as file:
                return json.load(file)["keybindings"]
        except Exception as e:
            print( f"Settings Path Manager: {self._KEY_BINDINGS_FILE}\n\t\t{repr(e)}" )
            return {}

    def load_context_menu_data(self):
        try:
            with open(self._CONTEXT_MENU) as file:
                return json.load(file)
        except Exception as e:
            print( f"Settings Path Manager: {self._CONTEXT_MENU}\n\t\t{repr(e)}" )
            return {}

    def load_settings(self):
        if not path.exists(self._CONFIG_FILE):
            return None

        with open(self._CONFIG_FILE) as file:
            data          = json.load(file)
            data["load_defaults"] = False
            return data

    def save_settings(self, settings: any):
        with open(self._CONFIG_FILE, 'w') as outfile:
            json.dump(settings.as_dict(), outfile, separators=(',', ':'), indent=4)