# Python imports
import os
from os import path

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Vte

# Application imports



class VteWidgetException(Exception):
    ...



class VteWidget(Vte.Terminal):
    """
        https://stackoverflow.com/questions/60454326/how-to-implement-a-linux-terminal-in-a-pygtk-app-like-vscode-and-pycharm-has
    """

    def __init__(self):
        super(VteWidget, self).__init__()

        self._USER_HOME: str = path.expanduser('~')

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()
        self._do_session_spawn()

        self.show()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("vte-widget")

        self.set_clear_background(False)
        self.set_hexpand(True)
        self.set_enable_sixel(True)
        self.set_cursor_shape( Vte.CursorShape.IBEAM )
        self.set_audible_bell(False)
        self.set_scroll_on_output(True)

    def _setup_signals(self):
        self.connect("commit", self._handle_commit)
        self.connect("current-directory-uri-changed", self._handle_path_change)
        self.connect("selection-changed", self._handle_selection)
        self.connect("button-press-event", self._on_button_press)
        self.connect("key-press-event", self._on_key_press)
        self.connect("key-release-event", self._on_key_release)
        self.connect("destroy", self._handle_destroy)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def _do_session_spawn(self):
        env_dict    = os.environ.copy()
        existing_pc = env_dict.get("PROMPT_COMMAND", "")
        # Note: Needed for 'current-directory-uri-changed' to work.
        #       Make sure user .bashrc doesn't affect it...
        osc7        = 'printf "\\033]7;file://%s%s\\007" "$PWD"'

        env_dict.update({
            "LC_ALL": "C",
            "TERM": "xterm-256color",
            "HISTFILE": "/dev/null",
            "HISTSIZE": "0",
            "HISTFILESIZE": "0",
            "PS1": "\\h@\\u \\W -->: ",
            "PROMPT_COMMAND": f"{osc7};{existing_pc}" if existing_pc else osc7,
        })

        env = [f"{k}={v}" for k, v in env_dict.items()]

        self.spawn_async(
            Vte.PtyFlags.DEFAULT,
            self._USER_HOME,
            ["/bin/bash"],
            env,
            GLib.SpawnFlags.DEFAULT,
            None, None, -1, None, None,
        )

        self.set_scrollback_lines(15000)

    def _handle_destroy(self, terminal):
        logger.debug("Destroying terminal...")
        terminal.disconnect_by_func(terminal._handle_commit)
        terminal.disconnect_by_func(terminal._handle_path_change)
        terminal.disconnect_by_func(terminal._handle_selection)
        terminal.disconnect_by_func(terminal._on_button_press)
        terminal.disconnect_by_func(terminal._on_key_press)
        terminal.disconnect_by_func(terminal._on_key_release)
        terminal.disconnect_by_func(terminal._handle_destroy)

    def _handle_commit(self, terminal, text, size):
        ...

    def _handle_selection(self, *args):
        if self.get_has_selection():
            self.copy_primary()

    def _on_button_press(self, widget, event):
        if event.button == 2:  # middle click
            self.paste_clipboard()
            return True

    def _on_key_press(self, widget, event):
        ctrl_pressed  = event.state & Gdk.ModifierType.CONTROL_MASK
        shift_pressed = event.state & Gdk.ModifierType.SHIFT_MASK

        if ctrl_pressed:
            if shift_pressed:
                if event.keyval in [Gdk.KEY_C, Gdk.KEY_V]:
                    if event.keyval == Gdk.KEY_C:
                        self.copy_clipboard()
                    elif event.keyval == Gdk.KEY_V:
                        self.paste_clipboard()

                    return True

            if event.keyval in [
                Gdk.KEY_period, Gdk.KEY_t, Gdk.KEY_w, Gdk.KEY_Up, Gdk.KEY_Down
            ]:
                if event.keyval == Gdk.KEY_period:
                    if hasattr(self, "hide_view"):
                        GLib.timeout_add(200, self.hide_view)
                elif event.keyval == Gdk.KEY_t:
                    if hasattr(self, "create_terminal"):
                        self.create_terminal()
                elif event.keyval == Gdk.KEY_w:
                    if hasattr(self, "close_terminal"):
                        self.close_terminal()
                elif event.keyval == Gdk.KEY_Up:
                    if hasattr(self, "prev_terminal"):
                        self.prev_terminal()
                elif event.keyval == Gdk.KEY_Down:
                    if hasattr(self, "next_terminal"):
                        self.next_terminal()

                return True

        return False

    def _on_key_release(self, widget, event):
        ...

    def _handle_path_change(self, terminal):
        if not hasattr(self, "label"): return

        uri = terminal.get_current_directory_uri().replace("file://", "")

        terminal.label.set_text(uri)
        terminal.label.set_tooltip_text(uri)

    def get_home_path(self):
        return self._USER_HOME

    def bind_label(self, label: Gtk.Label):
        self.label = label

    def run_command(self, cmd: str):
        self.feed_child_binary(bytes(cmd, 'utf8'))
