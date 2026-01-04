# Python imports

# Lib imports

# Application imports
from ..dto.observable_event import ObservableEvent



class ObservableMixin:
    observers = []

    def add_observer(self, observer: any):
        if not hasattr(observer, 'notification') or not callable(getattr(observer, 'notification')):
            raise ValueError(f"Observer '{observer}' must implement a `notification` method.")

        self.observers.append(observer)

    def remove_observer(self, observer: any):
        if not observer in self.observers: return

        self.observers.remove(observer)

    def notify_observers(self, event: ObservableEvent):
        for observer in self.observers:
            observer.notification(event)