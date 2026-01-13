# Python imports
from typing import Type, TypeVar, Any

# Lib imports

# Application imports



class SingletonError(Exception):
    pass



T = TypeVar('T', bound='SingletonRaised')

class SingletonRaised:
    _instance = None

    def __new__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        if cls._instance is not None:
            raise SingletonError(f"'{cls.__name__}' is a Singleton. Cannot create a new instance...")

        cls._instance = super(SingletonRaised, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._instance is not None:
            return
