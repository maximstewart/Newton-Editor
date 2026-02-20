# Python imports

# Lib imports
import gi
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2

# Application imports



class WebkitUISettings(WebKit2.Settings):
    def __init__(self):
        super(WebkitUISettings, self).__init__()
        
        self._set_default_settings()


    # Note: Highly insecure setup but most "app" like setup I could think of.
    #       Audit heavily any scripts/links ran/clicked under this setup! 
    def _set_default_settings(self):
        self.set_enable_xss_auditor(True)
        self.set_enable_hyperlink_auditing(True)
        # self.set_enable_xss_auditor(False)
        # self.set_enable_hyperlink_auditing(False)
        self.set_allow_file_access_from_file_urls(True)
        self.set_allow_universal_access_from_file_urls(True)

        self.set_enable_page_cache(False)
        self.set_enable_offline_web_application_cache(False)
        self.set_enable_html5_local_storage(False)
        self.set_enable_html5_database(False)

        self.set_enable_fullscreen(False)
        self.set_print_backgrounds(False)
        self.set_enable_tabs_to_links(False)
        self.set_enable_developer_extras(True)
        self.set_enable_webrtc(True)
        self.set_enable_webaudio(True)
        self.set_enable_accelerated_2d_canvas(True)

        self.set_user_agent(
            f"Mozilla/5.0 (macOS, AArch64) {APP_NAME}/1.0 Chrome/140.0.0 AppleWebKit/537.36 Safari/537.36"
        )

    # Note: Most "browser" like setup I could think of.
    def other_set_default_settings(self):
        # Usability
        self.set_property('enable-fullscreen', True)
        self.set_property('print-backgrounds', True)
        self.set_property('enable-frame-flattening', False)
        self.set_property('enable-plugins', True)
        self.set_property('enable-java', False)
        self.set_property('enable-resizable-text-areas', True)
        self.set_property('zoom-text-only', False)
        self.set_property('enable-smooth-scrolling', True)
        self.set_property('enable-back-forward-navigation-gestures', False)
        self.set_property('media-playback-requires-user-gesture', False)
        self.set_property('enable-tabs-to-links', True)
        self.set_property('enable-caret-browsing', False)

        # Security
        # self.set_property('user-agent', 'Mozilla/5.0 (X11; Generic; Linux x86-64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Safari/605.1.15')
        self.set_property('user-agent', f"Mozilla/5.0 (macOS, AArch64) {APP_NAME}/1.0 Chrome/140.0.0 AppleWebKit/537.36 Safari/537.36")
        self.set_property('enable-private-browsing', False)
        self.set_property('enable-xss-auditor', True)
        self.set_property('enable-hyperlink-auditing', False)
        self.set_property('enable-site-specific-quirks', True)
        self.set_property('enable-offline-web-application-cache', True)
        self.set_property('enable-page-cache', True)
        self.set_property('allow-modal-dialogs', True)
        self.set_property('enable-html5-local-storage', True)
        self.set_property('enable-html5-database', True)
        self.set_property('allow-file-access-from-file-urls', True)
        self.set_property('allow-universal-access-from-file-urls', False)
        self.set_property('enable-dns-prefetching', False)

        # Media stuff
        self.set_hardware_acceleration_policy(0)
        # self.set_property('hardware-acceleration-policy', 'on-demand')
        self.set_property('enable-webgl', True)
        self.set_property('enable-webaudio', True)
        self.set_property('enable-accelerated-2d-canvas', True)
        self.set_property('auto-load-images', True)
        self.set_property('enable-media-capabilities', True)
        self.set_property('enable-media-stream', True)
        self.set_property('enable-mediasource', True)
        self.set_property('enable-encrypted-media', True)
        self.set_property('media-playback-allows-inline', True)

        # JS
        self.set_property('enable-javascript', True)
        self.set_property('enable-javascript-markup', True)
        self.set_property('javascript-can-access-clipboard', False)
        self.set_property('javascript-can-open-windows-automatically', False)

        # Debugging
        self.set_property('enable-developer-extras', False)
        self.set_property('enable-write-console-messages-to-stdout', False)
        self.set_property('draw-compositing-indicators', False)
        self.set_property('enable-mock-capture-devices', False)
        self.set_property('enable-spatial-navigation', False)
