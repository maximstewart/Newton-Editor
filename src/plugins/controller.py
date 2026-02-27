# Python imports
import os
import sys
import importlib
import traceback

from concurrent.futures import ThreadPoolExecutor
from os.path import join
from os.path import isdir

# Lib imports
import gi
from gi.repository import GLib

# Application imports
from libs.controllers.controller_base import ControllerBase

from libs.dto.plugins.manifest_meta import ManifestMeta

from libs.dto.base_event import BaseEvent

from .manifest_manager import ManifestManager
from .plugins_controller_mixin import PluginsControllerMixin
from .plugin_reload_mixin import PluginReloadMixin
from .plugin_context import PluginContext



class PluginsControllerException(Exception):
    ...



class PluginsController(ControllerBase, PluginsControllerMixin, PluginReloadMixin):
    """ PluginsController controller """

    def __init__(self):
        super(PluginsController, self).__init__()

        # path                      = os.path.dirname(os.path.realpath(__file__))
        # sys.path.insert(0, path)  # NOTE: I think I'm not using this correctly...

        self._plugin_collection: list           = []

        self._plugins_path: str                 = settings_manager.path_manager.get_plugins_path()
        self._manifest_manager: ManifestManager = ManifestManager()

        self._set_plugins_watcher()


    def _controller_message(self, event: BaseEvent):
        for manifest_meta in self._plugin_collection:
            manifest_meta.instance._controller_message(event)

    def _collect_search_locations(self, path: str, locations: list):
        locations.append(path)
        for file in os.listdir(path):
            _path = os.path.join(path, file)
            if os.path.isdir(_path):
                self._collect_search_locations(_path, locations)

    def _load_plugins(
        self,
        manifest_metas: list = [],
        is_pre_launch: bool  = False
    ):
        parent_path = os.getcwd()

        for manifest_meta in manifest_metas:
            try:
                path,    \
                folder,  \
                manifest = manifest_meta.path, manifest_meta.folder, manifest_meta.manifest
                target   = join(path, "plugin.py")

                if not os.path.exists(target):
                    raise PluginsControllerException(
                        "Invalid Plugin Structure: Plugin doesn't have 'plugin.py'. Aboarting load..."
                    )

                module = self._load_plugin_module(path, folder, target)

                self._handle_plugin_execute(is_pre_launch, module, manifest_meta)
            except PluginsControllerException as e:
                logger.info(f"Malformed Plugin: Not loading -->: '{manifest_meta.folder}' !")
                logger.debug(f"Trace: {traceback.print_exc()}")

        os.chdir(parent_path)

    def _load_plugin_module(self, path, folder, target):
        os.chdir(path)

        locations = []
        self._collect_search_locations(path, locations)

        spec   = importlib.util.spec_from_file_location(folder, target, submodule_search_locations = locations)
        module = importlib.util.module_from_spec(spec)
        sys.modules[folder] = module
        spec.loader.exec_module(module)

        return module

    def _handle_plugin_execute(
        self, is_pre_launch: bool, module, manifest_meta
    ):
        if not is_pre_launch:
            GLib.idle_add(
                self._run_with_pool, module, manifest_meta
            )
            return

        self._run_with_pool(module, manifest_meta)

    def _run_with_pool(self, module: type, manifest_meta: ManifestMeta):
        with ThreadPoolExecutor(max_workers = 1) as executor:
            future = executor.submit(self.execute_plugin, module, manifest_meta)
            future.add_done_callback(self._handle_future_exception)

    def _handle_future_exception(self, future):
        try:
            future.result()
        except Exception:
            logger.exception("Plugin crashed during execution...")

    def pre_launch_plugins(self) -> None:
        logger.info(f"Loading pre-launch plugins...")
        manifest_metas: list = self._manifest_manager.get_pre_launch_plugins()
        self._load_plugins(manifest_metas, is_pre_launch = True)

    def post_launch_plugins(self) -> None:
        logger.info(f"Loading post-launch plugins...")
        manifest_metas: list = self._manifest_manager.get_post_launch_plugins()
        self._load_plugins(manifest_metas)

    def execute_plugin(self, module: type, manifest_meta: ManifestMeta):
        plugin                               = module.Plugin()
        plugin.plugin_context: PluginContext = self.create_plugin_context()

        manifest               = manifest_meta.manifest
        manifest_meta.instance = plugin

        if manifest.requests.bind_keys:
            keybindings.append_bindings( manifest.requests.bind_keys )

        manifest_meta.instance.load()
        manifest_meta.instance.run()

        self._plugin_collection.append(manifest_meta)

    def create_plugin_context(self):
        plugin_context: PluginContext                = PluginContext()

        plugin_context.requests_ui_element: callable = self.requests_ui_element
        plugin_context.message: callable             = self.message
        plugin_context.message_to: callable          = self.message_to
        plugin_context.message_to_selected: callable = self.message_to_selected
        plugin_context.emit: callable                = event_system.emit
        plugin_context.emit_and_await: callable      = event_system.emit_and_await
        plugin_context.register_controller: callable = self.register_controller

        return plugin_context


plugins_controller = PluginsController()
