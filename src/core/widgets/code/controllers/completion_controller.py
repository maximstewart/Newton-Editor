# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')

from gi.repository import GLib
from gi.repository import GtkSource

# Application imports
from libs.controllers.controller_base import ControllerBase
from libs.event_factory import Event_Factory, Code_Event_Types



class CompletionController(ControllerBase):
    def __init__(self):
        super(CompletionController, self).__init__()

        self._completers: list[GtkSource.Completion]             = []
        self._providers: dict[str, GtkSource.CompletionProvider] = {}

    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.RegisterProviderEvent):
            self.register_provider(
                event.provider_name,
                event.provider,
                event.language_ids
            )
        elif isinstance(event, Code_Event_Types.AddedNewFileEvent):
            self.provider_process_file_load(event)
        elif isinstance(event, Code_Event_Types.RemovedFileEvent):
            self.provider_process_file_close(event)
        elif isinstance(event, Code_Event_Types.SavedFileEvent):
            self.provider_process_file_save(event)
        elif isinstance(event, Code_Event_Types.TextChangedEvent):
            self.provider_process_file_change(event)
        # elif isinstance(event, Code_Event_Types.RequestCompletionEvent):
        #     self.request_unbound_completion( event.view.get_completion() )


    def register_completer(self, completer: GtkSource.Completion):
        self._completers.append(completer)

        for provider in self._providers.values():
            completer.add_provider(provider)

    def unregister_completer(self, completer: GtkSource.Completion):
        self._completers.remove(completer)

    def register_provider(
        self,
        provider_name: str,
        provider: GtkSource.CompletionProvider,
        language_ids: list = []
    ):
        self._providers[provider_name] = provider

        for completer in self._completers:
            completer.add_provider(provider)

    def unregister_provider(self, provider_name: str):
        provider = self._providers[provider_name]
        del self._providers[provider_name]

        for completer in self._completers:
            completer.remove_provider(provider)

    def provider_process_file_load(self, event: Code_Event_Types.AddedNewFileEvent):
        for provider in self._providers.values():
            # if provider.get_name() == "Words Completion":
            #    provider.register(event.file.buffer)
            provider.response_cache.process_file_load(event)

    def provider_process_file_close(self, event: Code_Event_Types.RemovedFileEvent):
        for provider in self._providers.values():
            provider.response_cache.process_file_close(event)

    def provider_process_file_save(self, event: Code_Event_Types.SavedFileEvent):
        for provider in self._providers.values():
            provider.response_cache.process_file_save(event)

    def provider_process_file_change(self, event: Code_Event_Types.TextChangedEvent):
        for provider in self._providers.values():
            provider.response_cache.process_file_change(event)

    def request_unbound_completion(self, completer: GtkSource.Completion):
        completer.start(
            [ *self._providers.values() ],
            completer.create_context()
        )
