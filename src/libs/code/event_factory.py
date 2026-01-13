# Python imports
import inspect
from typing import Dict, Type
import re

# Lib imports

# Application imports
from ..singleton import Singleton
from .dto.code import CodeEvent
from .dto import code



class EventFactory(Singleton):
    def __init__(self):
        self._event_classes: Dict[str, Type[CodeEvent]] = {}

        self._auto_register_events()

    def register_event(self, event_type: str, event_class: Type[CodeEvent]):
        self._event_classes[event_type] = event_class

    def create_event(self, event_type: str, **kwargs) -> CodeEvent:
        if event_type not in self._event_classes:
            raise ValueError(f"Unknown event type: {event_type}")

        event_class = self._event_classes[event_type]
        event = event_class()

        for key, value in kwargs.items():
            if not hasattr(event, key):
                raise ValueError(f"Event class {event_class.__name__} has no attribute '{key}'")

            setattr(event, key, value)

        return event

    def _auto_register_events(self):
        for name, obj in code.__dict__.items():
            if not self._is_valid_event_class(obj): continue

            event_type = self._class_name_to_event_type(name)
            self.register_event(event_type, obj)

        logger.debug(f"Auto-registered {len(self._event_classes)} event types")

    def _is_valid_event_class(self, obj) -> bool:
        return (
            inspect.isclass(obj)       and
            issubclass(obj, CodeEvent) and
            obj != CodeEvent
        )

    def _class_name_to_event_type(self, class_name: str) -> str:
        base_name = class_name[:-5] if class_name.endswith('Event') else class_name
        return re.sub(r'(?<!^)(?=[A-Z])', '_', base_name).lower()

    def create_cursor_moved(self, **kwargs):
        return self.create_event("cursor_moved", **kwargs)

    def create_text_changed(self, **kwargs):
        return self.create_event("text_changed", **kwargs)

    def create_focused_view(self, **kwargs):
        return self.create_event("focused_view", **kwargs)

    def create_modified_changed(self, **kwargs):
        return self.create_event("modified_changed", **kwargs)

    def create_get_command_system(self, **kwargs):
        return self.create_event("get_command_system", **kwargs)

    def create_file_path_set(self, **kwargs):
        return self.create_event("file_path_set", **kwargs)

    def create_text_inserted(self, **kwargs):
        return self.create_event("text_inserted", **kwargs)

    def create_set_active_file(self, **kwargs):
        return self.create_event("set_active_file", **kwargs)

    def create_added_new_file(self, **kwargs):
        return self.create_event("added_new_file", **kwargs)

    def create_popped_file(self, **kwargs):
        return self.create_event("popped_file", **kwargs)

    def create_get_file(self, **kwargs):
        return self.create_event("get_file", **kwargs)

    def create_get_swap_file(self, **kwargs):
        return self.create_event("get_swap_file", **kwargs)

    def create_remove_file(self, **kwargs):
        return self.create_event("remove_file", **kwargs)

    def create_removed_file(self, **kwargs):
        return self.create_event("removed_file", **kwargs)


Event_Factory       = EventFactory()
Event_Factory_Types = code
