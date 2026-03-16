# Python imports

# Lib imports

# Application imports
from .base_handler import BaseHandler
from .default import DefaultHandler



class ResponseRegistry:
    def __init__(self):

        self._instances: dict         = {}
        self._lang_handlers: dict     = {
            "default": DefaultHandler
        }


    def set_event_hub(self, emit, emit_to, provider = None):
        self.emit = emit
        self.emit_to = emit_to
        self._provider = provider


    def _get_instance(self, handler_cls: type[BaseHandler]) -> BaseHandler:
        if handler_cls in self._instances: return self._instances[handler_cls]

        self._instances[handler_cls] = handler_cls()

        return self._instances[handler_cls]

    def register_handler(self, lang_id: str, handler_cls: type[BaseHandler]):
        self._lang_handlers[lang_id] = handler_cls

    def unregister_handler(self, lang_id: str, handler_cls: type[BaseHandler]):
        del self._lang_handlers[lang_id]

    def get_handler(self, lang_id: str = "", method: str = ""):
        handler_cls = self._lang_handlers.get(
            lang_id, self._lang_handlers.get("default", DefaultHandler)
        )
        
        if not handler_cls: return None

        return self._get_instance(handler_cls)

    def close_handler(self, lang_id: str):
        if not lang_id in self._lang_handlers: return

        handler_cls = self._lang_handlers[lang_id]
        self._instances.pop(handler_cls, None)
