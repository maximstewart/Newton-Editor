# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from libs.dto.states import SourceViewStates

from .source_view_base_state import SourceViewsBaseState



class SourceViewsIndependentState(SourceViewsBaseState):
    def __init__(self):
        super(SourceViewsIndependentState, self).__init__()
