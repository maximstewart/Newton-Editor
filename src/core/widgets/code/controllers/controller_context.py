# Python imports

# Lib imports

# Application imports
from libs.dto.code.code_event import CodeEvent



class ControllerContextException(Exception):
    ...



class ControllerContext:
    def __init__(self):
        super(ControllerContext, self).__init__()


    def message_to(self, name: str, event: CodeEvent):
        raise ControllerContextException("Controller Context 'message_to' must be overriden by Controller Manager...")

    def message_all(self, event: CodeEvent):
        raise ControllerContextException("Controller Context 'message_all' must be overriden by Controller Manager...")
