# Python imports
import os
import sys
import importlib
import traceback
from os.path import join
from os.path import isdir

# Lib imports
import gi
from gi.repository import GLib

# Application imports
from .dto.manifest_meta import ManifestMeta
from .plugin_reload_mixin import PluginReloadMixin
from .manifest_manager import ManifestManager



class InvalidPluginException(Exception):
    ...



class PluginsController(PluginReloadMixin):
    """PluginsController controller"""

    def __init__(self):
        # path                      = os.path.dirname(os.path.realpath(__file__))
        # sys.path.insert(0, path)  # NOTE: I think I'm not using this correctly...

        self._plugin_collection   = []

        self._plugins_path        = settings_manager.path_manager.get_plugins_path()
        self._manifest_manager    = ManifestManager()

        self._set_plugins_watcher()


    def pre_launch_plugins(self) -> None:
        logger.info(f"Loading pre-launch plugins...")
        manifest_metas: [] = self._manifest_manager.get_pre_launch_manifests()
        self._load_plugins(manifest_metas, is_pre_launch = True)

    def post_launch_plugins(self) -> None:
        logger.info(f"Loading post-launch plugins...")
        manifest_metas: [] = self._manifest_manager.get_post_launch_plugins()
        self._load_plugins(manifest_metas)

    def _load_plugins(
        self,
        manifest_metas: [] = [],
        is_pre_launch: bool = False
    ) -> None:
        parent_path = os.getcwd()

        for manifest_meta in manifest_metas:
            path, folder, manifest = manifest_meta.path, manifest_meta.folder, manifest_meta.manifest

            try:
                target = join(path, "plugin.py")
                if not os.path.exists(target):
                    raise InvalidPluginException("Invalid Plugin Structure: Plugin doesn't have 'plugin.py'. Aboarting load...")

                module = self.load_plugin_module(path, folder, target)

                if is_pre_launch:
                    self.execute_plugin(module, manifest_meta)
                else:
                    GLib.idle_add(self.execute_plugin, module, manifest_meta)
            except Exception as e:
                logger.info(f"Malformed Plugin: Not loading -->: '{folder}' !")
                logger.debug("Trace: ", traceback.print_exc())

        os.chdir(parent_path)

    def load_plugin_module(self, path, folder, target):
        os.chdir(path)

        locations = []
        self.collect_search_locations(path, locations)

        spec   = importlib.util.spec_from_file_location(folder, target, submodule_search_locations = locations)
        module = importlib.util.module_from_spec(spec)
        sys.modules[folder] = module
        spec.loader.exec_module(module)

        return module

    def collect_search_locations(self, path: str, locations: list):
        locations.append(path)
        for file in os.listdir(path):
            _path = os.path.join(path, file)
            if os.path.isdir(_path):
                self.collect_search_locations(_path, locations)

    def execute_plugin(self, module: type, manifest_meta: ManifestMeta):
        manifest               = manifest_meta.manifest
        manifest_meta.instance = module.Plugin()

        if manifest.requests.ui_target:
            builder      = settings_manager.get_builder()
            ui_target    = manifest.requests.ui_target
            ui_target_id = manifest.requests.ui_target_id

            if not ui_target == "other":
                ui_target = builder.get_object(ui_target)
            else:
                if not ui_target_id:
                    raise InvalidPluginException('Invalid "ui_target_id" given in requests. Must have one if setting "ui_target" to "other"...')

                ui_target = builder.get_object(ui_target_id)

            if not ui_target:
                raise InvalidPluginException('Unknown "ui_target" given in requests.')

            ui_element = manifest_meta.instance.generate_reference_ui_element()

            ui_target.add(ui_element)

        if manifest.requests.pass_ui_objects:
            manifest_meta.instance.set_ui_object_collection(
                [ builder.get_object(obj) for obj in manifest.requests.pass_ui_objects ]
            )

        if manifest.requests.pass_events:
            manifest_meta.instance.set_event_system(event_system)
            manifest_meta.instance.subscribe_to_events()

        if manifest.requests.bind_keys:
            keybindings.append_bindings( manifest.requests.bind_keys )

        manifest_meta.instance.run()
        self._plugin_collection.append(manifest_meta)
