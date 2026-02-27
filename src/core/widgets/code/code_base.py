# Python imports

# Lib imports

# Application imports
from plugins import plugins_controller

from libs.controllers.controller_manager import ControllerManager

from .controllers.files_controller import FilesController
from .controllers.commands_controller import CommandsController
from .controllers.completion_controller import CompletionController
from .controllers.views.source_views_controller import SourceViewsController



class CodeBase:
    def __init__(self):
        super(CodeBase, self).__init__()

        self.controller_manager: ControllerManager = ControllerManager()

        self._subscribe_to_events()
        self._load_controllers()


    def _subscribe_to_events(self):
        event_system.subscribe("handle-file", self._load_ipc_file)
        event_system.subscribe("handle-files", self._load_ipc_files)

    def _load_controllers(self):
        files_controller        = FilesController()
        commands_controller     = CommandsController()
        completion_controller   = CompletionController()
        source_views_controller = SourceViewsController()

        # self.controller_manager.register_controller("base", self)
        self.controller_manager.register_controller("files", files_controller)
        self.controller_manager.register_controller("commands", commands_controller)
        self.controller_manager.register_controller("completion", completion_controller)
        self.controller_manager.register_controller("source_views", source_views_controller)
        self.controller_manager.register_controller("plugins", plugins_controller)
        self.controller_manager.register_controller("widgets", widget_registery)

    def create_source_view(self):
        source_view = self.controller_manager["source_views"].create_source_view()
        self.controller_manager["completion"].register_completer(
            source_view.get_completion()
        )

        return source_view

    def first_map_load(self):
        self.controller_manager["source_views"].first_map_load()

    def _load_ipc_file(self, fpath: str):
        active_view = self.controller_manager["source_views"].signal_mapper.active_view
        uris        = [ f"file://{fpath}" ]
        active_view._on_uri_data_received(uris)

    def _load_ipc_files(self, uris: list):
        active_view = self.controller_manager["source_views"].signal_mapper.active_view
        active_view._on_uri_data_received(uris)
