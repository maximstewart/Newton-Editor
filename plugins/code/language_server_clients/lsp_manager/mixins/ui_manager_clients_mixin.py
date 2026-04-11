# Python imports
import json

# Lib imports
import gi

from gi.repository import GObject

# Application imports



class UIManagerClientsMixin:
    def _create_client(self, widget, sibling):
        if not self.source_view: return

        buffer  = self.source_view.get_buffer()
        lang_id = self.combo_box.get_active_text()

        if not lang_id: return

        workspace_dir = self.path_entry.get_text()
        self.emit('create-client', lang_id, workspace_dir)

    def _close_client(self, widget, sibling):
        lang_id = self.combo_box.get_active_text()

        if not lang_id: return

        self.emit('close-client', lang_id)

    def set_source_view_text(self, workspace_dir: str):
        lang_id = self.combo_box.get_active_text()

        if not lang_id: return

        json_str = self.client_configs[lang_id]\
                        .replace("{workspace.folder}", workspace_dir)\
                        .replace("{user.home}", self._USER_HOME)

        self.source_view.get_buffer().set_text(json_str, -1)

    def add_client_listing(self, lang_id: str, lang_config: str):
        self.combo_box.append_text(lang_id)
        self.client_configs[lang_id] = lang_config

    def remove_client_listing(self, lang_id: str):
        model = self.combo_box.get_model()

        for i, row in enumerate(model):
            if row[0] == lang_id:
                self.combo_box.remove(i)
                break

        self.client_configs.pop(lang_id, None)

    def toggle_client_buttons(self, show_close: bool):
        self.create_client_bttn.set_visible(not show_close)
        self.close_client_bttn.set_visible(show_close)

    def get_init_opts(self, lang_id: str) -> dict:
        if not lang_id or lang_id not in self.client_configs: return {}

        try:
            buffer      = self.source_view.get_buffer()
            json_str    = buffer.get_text(*buffer.get_bounds(), -1)
            lang_config = json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON for {lang_id}: {e}")
            return {}

        return lang_config.get("initialization-options", {})
