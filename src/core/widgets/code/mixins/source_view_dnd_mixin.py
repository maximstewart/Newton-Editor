# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class SourceViewDnDMixin:

    def _set_up_dnd(self):
        PLAIN_TEXT_TARGET_TYPE = 70
        URI_TARGET_TYPE        = 80
        text_target = Gtk.TargetEntry.new('text/plain', Gtk.TargetFlags(0), PLAIN_TEXT_TARGET_TYPE)
        uri_target  = Gtk.TargetEntry.new('text/uri-list', Gtk.TargetFlags(0), URI_TARGET_TYPE)
        targets     = [ text_target, uri_target ]

        self.drag_dest_set_target_list(targets)

    def _on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        if info == 70: return

        if info == 80:
            uris = data.get_uris()

            if len(uris) == 0:
                uris = data.get_text().split("\n")

            self._on_uri_data_received(uris)

    def _on_uri_data_received(self, uris: []):
            uri = uris.pop(0)
            self.command.exec_with_args("dnd_load_file_to_buffer", (self, uri))

            if len(uris) == 0: return

            self.command.exec_with_args("dnd_load_files", (self, uris))
