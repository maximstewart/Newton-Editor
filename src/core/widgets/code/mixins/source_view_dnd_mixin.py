# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
#gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
#from gi.repository import Gdk


# Application imports



class SourceViewDnDMixin:

    def _set_up_dnd(self):
        URI_TARGET_TYPE        = 10
        PLAIN_TEXT_TARGET_TYPE = 50

        uri_target  = Gtk.TargetEntry.new(
            'text/uri-list', Gtk.TargetFlags(0), URI_TARGET_TYPE
        )
        text_target = Gtk.TargetEntry.new(
            'text/plain', Gtk.TargetFlags(0), PLAIN_TEXT_TARGET_TYPE
        )
        targets     = Gtk.TargetList.new([ uri_target, text_target ])

        self.drag_dest_set_target_list(targets)

    def _on_drag_data_received(
        self, widget, drag_context, x, y, data, info, time
    ):
        target = data.get_target().name()

        if (info == 10) or (target == "text/uri-list"):
            uris = data.get_uris()
            if not uris:
                uris = data.get_text().split("\n")

            self._on_uri_data_received(uris)

            drag_context.finish(True, False, time)

            return
        elif (info == 50) or (target == "text/plain"):
            ...
        else:
            logger.info(f"DnD Dropped File Type: {target}")

        drag_context.finish(False, False, time)

    def _on_uri_data_received(self, uris: list[str]):
            uris = self.command.filter_out_loaded_files(uris)
            if not uris: return

            uri = uris.pop(0)

            self.command.exec_with_args("dnd_load_file_to_buffer", self, uri)

            if not uris: return

            self.command.exec_with_args("dnd_load_files", self, uris)
