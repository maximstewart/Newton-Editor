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
        for name, obj in events:
            if not self._is_valid_event_class(obj): continue

            event_type = self._class_name_to_event_type(name)
            self.register_event(event_type, obj)

        logger.debug(f"Registered {len(events)} event types:")

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


Event_Factory    = EventFactory()
Code_Event_Types = code
