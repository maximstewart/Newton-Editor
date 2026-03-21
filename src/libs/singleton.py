# Python imports
from typing import Type, TypeVar, Any

# Lib imports

# Application imports



class SingletonError(Exception):
    pass



T = TypeVar('T', bound = 'Singleton')



class Singleton:
    _instances = {}

    def __new__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        if cls in cls._instances: return cls._instances[cls]

        instance = super().__new__(cls)
        cls._instances[cls] = instance
        return instance

    @classmethod
    def destroy(cls):
        if cls in cls._instances:
            del cls._instances[cls]
