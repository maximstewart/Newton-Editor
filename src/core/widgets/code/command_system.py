# Python imports

# Lib imports

# Application imports
from . import commands



class CommandSystem:
    def __init__(self):
        super(CommandSystem, self).__init__()

        self.data: list = ()


    def set_data(self, *args, **kwargs):
        self.data = (args, kwargs)

    def exec(self, command: str) -> any:
        if not hasattr(commands, command): return
        method = getattr(commands, command)

        args, kwargs = self.data
        if kwargs:
            return method.execute(*args, kwargs)
        else:
            return method.execute(*args)

    def exec_with_args(self, command: str, args: list) -> any:
        if not hasattr(commands, command): return

        method = getattr(commands, command)
        return method.execute(*args)
