# Python imports

# Lib imports
import gi
from gi.repository import Gio

# Application imports



class PluginReloadMixin:
    _plugins_dir_watcher = None

    def _set_plugins_watcher(self) -> None:
        self._plugins_dir_watcher =                     \
            Gio.File.new_for_path( self._plugins_path ) \
            .monitor_directory(
                Gio.FileMonitorFlags.WATCH_MOVES,
                Gio.Cancellable()
            )

        self._plugins_dir_watcher.connect("changed", self._on_plugins_changed, ())

    def _on_plugins_changed(self,
        file_monitor, file,
        other_file = None,
        eve_type   = None,
        data       = None
    ):
        if eve_type is Gio.FileMonitorEvent.RENAMED:
            ...

        if eve_type in [Gio.FileMonitorEvent.CREATED, Gio.FileMonitorEvent.MOVED_IN]:
            self.add_plugin(file)

        if eve_type in [Gio.FileMonitorEvent.DELETED, Gio.FileMonitorEvent.MOVED_OUT]:
            self.remove_plugin(file)

    def add_plugin(self, file: str) -> None:
        logger.info(f"Adding plugin: {file.get_uri()}")
        uri           = file.get_uri()
        path          = uri.replace("file://", "")
        folder        = path.split("/")[-1]
        manifest_meta = self._manifest_manager.load(folder, path)

        self._load_plugins( [manifest_meta] )
        self.plugins_ui.add_row(manifest_meta, self.toggle_plugin_load_state)

    def remove_plugin(self, file: str) -> None:
        logger.info(f"Removing plugin: {file.get_uri()}")
        for manifest_meta in self._plugin_collection[:]:
            if not manifest_meta.folder in file.get_uri(): continue

            manifest_meta.instance.unload()
            manifest_meta.instance = None
            self._plugin_collection.remove(manifest_meta)
            self.plugins_ui.remove_row(manifest_meta)

            if manifest_meta in self._manifest_manager.pre_launch_manifests:
                self._manifest_manager.pre_launch_manifests.remove(manifest_meta)
            elif manifest_meta in self._manifest_manager.post_launch_manifests:
                self._manifest_manager.post_launch_manifests.remove(manifest_meta)
            elif manifest_meta in self._manifest_manager.manual_launch_manifests:
                self._manifest_manager.manual_launch_manifests.remove(manifest_meta)

            break
