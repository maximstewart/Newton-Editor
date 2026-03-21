# Python imports
import inspect
from typing import Dict, Type
import re

# Lib imports

# Application imports
from .singleton import Singleton

from .dto.base_event import BaseEvent
from .dto.code import events as code



class EventFactory(Singleton):
    def __init__(self):

        self._event_classes: Dict[str, Type[BaseEvent]] = {}

        self._auto_register_events( code.__dict__.items() )

    def register_event(self, event_type: str, event_class: Type[BaseEvent]):
        self._event_classes[event_type] = event_class

    def register_events(self, events: dict):
        i = 0
        for name, obj in events:
            if not self._is_valid_event_class(obj): continue

            event_type = self._class_name_to_event_type(name)

            self._event_classes[event_type] = obj
            Code_Event_Types.add_event_class(name, obj)
            i += 1

        logger.debug(f"Registered {i} event types:")

    def unregister_events(self, events: dict):
        i = 0
        for name, obj in events:
            if not self._is_valid_event_class(obj): continue

            event_type = self._class_name_to_event_type(name)

            del self._event_classes[event_type]
            Code_Event_Types.remove_event_class(name)
            i += 1

        logger.debug(f"Unregistered {i} event types:")

    def create_event(self, event_type: str, **kwargs) -> BaseEvent:
        if event_type not in self._event_classes:
            raise ValueError(f"Unknown event type: {event_type}")

        event_class = self._event_classes[event_type]
        event = event_class()

        for key, value in kwargs.items():
            if not hasattr(event, key):
                raise ValueError(f"Event class {event_class.__name__} has no attribute '{key}'")

            setattr(event, key, value)

        return event


    def _auto_register_events(self, events: dict):
        self.register_events(events)

    def _is_valid_event_class(self, obj) -> bool:
        return (
            inspect.isclass(obj)       and
            issubclass(obj, BaseEvent) and
            obj != BaseEvent
        )

    def _class_name_to_event_type(self, class_name: str) -> str:
        base_name = class_name[:-5] if class_name.endswith('Event') else class_name
        return re.sub(r'(?<!^)(?=[A-Z])', '_', base_name).lower()


class EventNamespace:
    """Dynamic namespace for event types."""

    def __init__(self):
        ...


    def _is_valid_event_class(self, obj) -> bool:
        return (inspect.isclass(obj) and issubclass(obj, BaseEvent) and obj != BaseEvent)

    def add_event_class(self, name: str, event_class: Type[BaseEvent]):
        setattr(self, name, event_class)

    def remove_event_class(self, name: str):
        delattr(self, name)



Code_Event_Types = EventNamespace()
Event_Factory    = EventFactory()

