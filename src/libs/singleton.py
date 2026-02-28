# Python imports
from typing import Type, TypeVar, Any

# Lib imports

# Application imports



class SingletonError(Exception):
    pass



T = TypeVar('T', bound='Singleton')

class Singleton:
    __instance = None

    def __new__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        if cls.__instance is not None:
            logger.debug(f"'{cls.__name__}' is a Singleton. Returning  instance...")
            return cls.__instance

        cls.__instance = super(Singleton, cls).__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if self.__instance is not None:
            return

        super(Singleton, self).__init__()
