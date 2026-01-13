# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GLib
from gi.repository import GtkSource

# Application imports
from ..event_factory import Event_Factory, Event_Factory_Types

from ..completion_providers.example_completion_provider import ExampleCompletionProvider
from ..completion_providers.lsp_completion_provider import LSPCompletionProvider

from .foundation.controller_base import ControllerBase



class CompletionController(ControllerBase):
    def __init__(self):
        super(CompletionController, self).__init__()

        self._completor: GtkSource.Completion     = None
        self._timeout_id: int                     = None
        self._lsp_provider: LSPCompletionProvider = LSPCompletionProvider()


    def _controller_message(self, event: Event_Factory_Types.CodeEvent):
        if isinstance(event, Event_Factory_Types.FocusedViewEvent):
            self._completor = event.view.get_completion()

            if not self._timeout_id: return

            GLib.source_remove(self._timeout_id)
            self._timeout_id = None
        elif isinstance(event, Event_Factory_Types.RequestCompletionEvent):
            self.request_completion()
        # elif isinstance(event, Event_Factory_Types.TextInsertedEvent):
        #     self.request_completion()

    def _process_request_completion(self):
        self._start_completion()

        self._timeout_id = None
        return False

    def _do_completion(self):
        if self._completor.get_providers():
            self._match_completion()
        else:
            self._start_completion()

    def _match_completion(self):
        """
            Note: Use IF providers were added to completion...
        """
        self._completion.match(
            self._completion.create_context()
        )


    def _start_completion(self):
        """
            Note: Use IF NO providers have been added to completion...
        """
        self._completor.start(
            [
                ExampleCompletionProvider(),
                self._lsp_provider
            ],
            self._completor.create_context()
        )


    def set_completer(self, completer):
        self._completor = completer

    def request_completion(self):
        if self._timeout_id:
            GLib.source_remove(self._timeout_id)

        self._timeout_id = GLib.timeout_add(
            800,
            self._process_request_completion
        )

    def register_provider(
        self,
        provider_name: str,
        provider: GtkSource.CompletionProvider, 
        priority: int = 0,
        language_ids: list = None
    ):
        """Register completion providers with priority and language filtering"""
        ...

    def unregister_provider(self, provider_name: str):
        """Remove completion providers"""
        ...
        
    def get_active_providers(self, language_id: str = None) -> list:
        """Get providers filtered by language"""
        ...
