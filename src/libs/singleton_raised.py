# Python imports

# Lib imports

# Application imports



class SingletonError(Exception):
    pass



class SingletonRaised:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            raise SingletonError(f"'{cls.__name__}' is a Singleton. Cannot create a new instance...")

        cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if cls._instance is not None:
            return
