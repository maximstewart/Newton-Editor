# Python imports
import types

# Lib imports

# Application imports
from .event_factory import Event_Factory, Code_Event_Types



class CommandSystem:
    def __init__(self, commands: dict | types.ModuleType):
        super(CommandSystem, self).__init__()

        self.commands: dict | types.ModuleType = commands
        self.data: tuple    = ()


    def set_data(self, *args, **kwargs):
        self.data = (args, kwargs)

    def exec(self, command: str) -> any:
        """
            The 'exec' method passes the default 'self.data' to commands where custom args are not needed.
            Ex: The 'code' widget has many internally created commands that
            only need 'source_view' and so 'set_data' is called to set that.
        """
        if not hasattr(self.commands, command): return
        method = getattr(self.commands, command)

        args, kwargs = self.data
        return method.execute(*args, **kwargs)

    def exec_with_args(self, command: str, *args, **kwargs) -> any:
        """
            The 'exec_with_args' method passes custom args with the understanding
            that the recipient has proper method signature to accept it- whether
            *args or **kwargs or something else entirely.
        """
        if not hasattr(self.commands, command): return

        method = getattr(self.commands, command)
        return method.execute(*args, **kwargs)

    def add_command(self, command_name: str, command: callable):
        setattr(self.commands, command_name, command)

    def remove_command(self, command_name: str, command: callable):
        if hasattr(self.commands, command_name):
            delattr(self.commands, command_name)
