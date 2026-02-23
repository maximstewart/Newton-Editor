# Python imports
from pathlib import Path
import json

# Lib imports
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import WebKit2

# Application imports
from libs.settings.webkit.webkit_ui_settings import WebkitUISettings
from libs.dto.base_event import BaseEvent


class WebkitUI(WebKit2.WebView):
    def __init__(self):
        super(WebkitUI, self).__init__()

        self._load_settings()
        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._setup_content_manager()

        self.show_all()


    def _setup_styling(self):
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_background_color( Gdk.RGBA(0, 0, 0, 0.0) )

    def _setup_signals(self):
        self.connect("context-menu", self._on_context_menu)

    def _subscribe_to_events(self):
        event_system.subscribe(f"ui-message", self.ui_message)

    def _load_settings(self):
        self.set_settings( WebkitUISettings() )

    def _setup_content_manager(self):
        content_manager = self.get_user_content_manager()
        content_manager.connect("script-message-received", self._process_js_message)
        content_manager.register_script_message_handler("backend")

    def _process_js_message(self, user_content_manager, js_result):
        js_value = js_result.get_js_value()
        message  = js_value.to_string()

        try:
            event = BaseEvent( **json.loads(message) )
            event_system.emit("handle-bridge-event", (event,))
        except Exception as e:
            logger.info(e)

    def _on_context_menu(self, web_view, context_menu, event, hit_test_result):
        action = Gio.SimpleAction.new("Developer Tools", None)
        item   = WebKit2.ContextMenuItem.new_from_gaction(action, "Developer Tools")

        def show_developer_tools(action, parameter):
            inspector = self.get_inspector()
            inspector.show()

        action.connect("activate", show_developer_tools)

        context_menu.append(item)

    def load_url(self, url: str = ""):
        if not url:
            url = "https://duckduckgo.com/"

        self.load_uri(url)

    def load_context_base_path(self, path: str = ""):
        if not path:
            path   = settings_manager.path_manager.get_context_path()

        base_path  = Path(path)
        index_file = base_path / "index.html"

        if not index_file.exists():
            raise FileNotFoundError(f"index.html not found in {base_path}")

        try:
            data = index_file.read_text(encoding = "utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to read {index_file}: {e}")

        self.load_html(
            content = data,
            base_uri = index_file.as_uri()
        )

    def ui_message(self, message, mtype):
        command = f"displayMessage('{message}', '{mtype}', '3')"
        self.run_javascript(command, None, None)

    def run_javascript(self, script, cancellable, callback):
        logger.debug(script)
        super().run_javascript(script, cancellable, callback)
