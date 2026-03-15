# Python imports

# Lib imports

# Application imports



class BaseHandler:
    def __init__(self):
        self.context        = None
        self.response_cache = None


    def set_context(self, context):
        self.context = context

    def set_response_cache(self, response_cache):
        self.response_cache = response_cache

    @property
    def emit(self):
        return self.context.emit

    @property
    def emit_to(self):
        return self.context.emit_to

    def handle(self, method: str, response, controller):
        pass
