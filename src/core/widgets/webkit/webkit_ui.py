# Python imports
import json

# Lib imports
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gdk
from gi.repository import WebKit2

# Application imports
from libs.settings.other.webkit_ui_settings import WebkitUISettings
from libs.dto.event import Event


class WebkitUI(WebKit2.WebView):
    def __init__(self):
        super(WebkitUI, self).__init__()

        self._setup_styling()
        self._subscribe_to_events()
        self._load_view()
        self._setup_content_manager()

        self.show_all()


    def _setup_styling(self):
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_background_color( Gdk.RGBA(0, 0, 0, 0.0) )

    def _subscribe_to_events(self):
        event_system.subscribe(f"ui-message", self.ui_message)

    def _load_settings(self):
        self.set_settings( WebkitUISettings() )

    def _load_view(self):
        path = settings_manager.get_context_path()
        data = None

        with open(f"{path}/index.html", "r") as f:
            data = f.read()

        self.load_html(content = data, base_uri = f"file://{path}/")

    def _setup_content_manager(self):
        content_manager = self.get_user_content_manager()
        content_manager.connect("script-message-received", self._process_js_message)
        content_manager.register_script_message_handler("backend")

    def _process_js_message(self, user_content_manager, js_result):
        js_value = js_result.get_js_value()
        message  = js_value.to_string()

        try:
            event = Event( **json.loads(message) )
            event_system.emit("handle-bridge-event", (event,))
        except Exception as e:
            logger.info(e)

    def ui_message(self, message, mtype):
        command = f"displayMessage('{message}', '{mtype}', '3')"
        self.run_javascript(command, None, None)

    def run_javascript(self, script, cancellable, callback):
        logger.debug(script)
        super().run_javascript(script, cancellable, callback)
