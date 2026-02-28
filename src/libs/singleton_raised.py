# Python imports
from typing import Type, TypeVar, Any

# Lib imports

# Application imports



class SingletonError(Exception):
    pass



T = TypeVar('T', bound='SingletonRaised')

class SingletonRaised:
    __instance = None

    def __new__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        if cls.__instance is not None:
            raise SingletonError(f"'{cls.__name__}' is a Singleton. Cannot create a new instance...")

        cls.__instance = super(SingletonRaised, cls).__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if self.__instance is not None:
            return
