# Python imports

# Lib imports

# Application imports
from .controllers.controller_manager import ControllerManager
from .controllers.files_controller import FilesController
from .controllers.tabs_controller import TabsController
from .controllers.commands_controller import CommandsController
from .controllers.completion_controller import CompletionController
from .controllers.source_views_controller import SourceViewsController

from .mini_view_widget import MiniViewWidget



class CodeBase:
    def __init__(self):
        super(CodeBase, self).__init__()

        self.controller_manager: ControllerManager = ControllerManager()
        self.miniview_widget: MiniViewWidget       = MiniViewWidget()

        self._load_controllers()


    def _load_controllers(self):
        files_controller        = FilesController()
        tabs_controller         = TabsController()
        commands_controller     = CommandsController()
        completion_controller   = CompletionController()
        source_views_controller = SourceViewsController()

        # self.controller_manager.register_controller("base", self)
        self.controller_manager.register_controller("files", files_controller)
        self.controller_manager.register_controller("tabs", tabs_controller)
        self.controller_manager.register_controller("commands", commands_controller)
        self.controller_manager.register_controller("completion", completion_controller)
        self.controller_manager.register_controller("source_views", source_views_controller)
        # self.controller_manager.register_controller("plugins", plugins_controller)

    def get_tabs_widget(self):
        return self.controller_manager["tabs"].get_tabs_widget()

    def get_mini_view_widget(self):
        return self.miniview_widget

    def create_source_view(self):
        return self.controller_manager["source_views"].create_source_view()

    def first_map_load(self):
        self.controller_manager["source_views"].first_map_load()
