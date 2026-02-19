# Python imports
import copy
import json

# Lib imports
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

# Application imports



class NoKeyState:
    held: dict     = {}
    released: dict = {}

class CtrlKeyState:
    held: dict     = {}
    released: dict = {}

class ShiftKeyState:
    held: dict     = {}
    released: dict = {}

class AltKeyState:
    held: dict     = {}
    released: dict = {}

class CtrlShiftKeyState:
    held: dict     = {}
    released: dict = {}

class CtrlAltKeyState:
    held: dict     = {}
    released: dict = {}

class AltShiftKeyState:
    held: dict     = {}
    released: dict = {}

class CtrlShiftAltKeyState:
    held: dict     = {}
    released: dict = {}



class KeyMapper:
    def __init__(self):
        super(KeyMapper, self).__init__()

        self.state   = NoKeyState
        self._map    = {
            NoKeyState:                                              NoKeyState(),
            NoKeyState | CtrlKeyState :                              CtrlKeyState(),
            NoKeyState | ShiftKeyState:                              ShiftKeyState(),
            NoKeyState | AltKeyState  :                              AltKeyState(),
            NoKeyState | CtrlKeyState | ShiftKeyState :              CtrlShiftKeyState(),
            NoKeyState | CtrlKeyState | AltKeyState   :              CtrlAltKeyState(),
            NoKeyState | AltKeyState  | ShiftKeyState :              AltShiftKeyState(),
            NoKeyState | CtrlKeyState | ShiftKeyState | AltKeyState: CtrlShiftAltKeyState(),
        }

        self.load_map()


    def load_map(self):
        self.states   = copy.deepcopy(self._map)
        bindings_file = f"{settings_manager.path_manager.get_home_config_path()}/code-key-bindings.json"

        with open(bindings_file, 'r') as f:
            data = json.load(f)["keybindings"]
            for command in data:
                self.map_command( command, data[command] )

    def re_map(self):
        self.states = copy.deepcopy(self._map)

    def map_command(self, command, entry):
        press_state = "held" if "held" in entry else "released"
        keyname     = entry[press_state]

        state       = NoKeyState
        if "<Control>" in keyname:
            state = state | CtrlKeyState
        if "<Shift>" in keyname:
            state = state | ShiftKeyState
        if "<Alt>" in keyname:
            state = state | AltKeyState

        keyname = keyname.replace("<Control>", "") \
                         .replace("<Shift>",   "") \
                         .replace("<Alt>",     "") \
                         .lower()

        getattr(self.states[state], press_state)[keyname] = command

    def _key_press_event(self, eve):
        keyname = Gdk.keyval_name(eve.keyval).lower()

        self._set_key_state(eve)
        if keyname in self.states[self.state].held:
            return self.states[self.state].held[keyname]

    def _key_release_event(self, eve):
        keyname = Gdk.keyval_name(eve.keyval).lower()

        self._set_key_state(eve)
        if keyname in self.states[self.state].released:
            return self.states[self.state].released[keyname]

    def _set_key_state(self, eve):
        modifiers  = Gdk.ModifierType(eve.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        is_control = True if modifiers & Gdk.ModifierType.CONTROL_MASK else False
        is_shift   = True if modifiers & Gdk.ModifierType.SHIFT_MASK else False

        try:
            is_alt = True if modifiers & Gdk.ModifierType.ALT_MASK else False
        except Exception:
            is_alt = True if modifiers & Gdk.ModifierType.MOD1_MASK else False

        self.state = NoKeyState
        if is_control:
            self.state = self.state | CtrlKeyState
        if is_shift:
            self.state = self.state | ShiftKeyState
        if is_alt:
            self.state = self.state | AltKeyState

    def is_control(self, eve):
        modifiers  = Gdk.ModifierType(eve.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        return True if modifiers & Gdk.ModifierType.CONTROL_MASK else False

    def is_shift(self, eve):
        modifiers  = Gdk.ModifierType(eve.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        return True if modifiers & Gdk.ModifierType.SHIFT_MASK else False

    def get_raw_keyname(self, eve):
        return Gdk.keyval_name(eve.keyval)
