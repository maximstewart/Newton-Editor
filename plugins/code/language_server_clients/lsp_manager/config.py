# Python imports
from os import path
import json

# Lib imports

# Application imports



LSP_HOST: str = "127.0.0.1"
LSP_PORT: int = 9999
LSP_CONNECT_TIMOUT: float = 5.0



def get_lsp_host_addr() -> str:
    return LSP_HOST

def get_lsp_host_port() -> int:
    return LSP_PORT

def get_lsp_connect_timout() -> float:
    return LSP_CONNECT_TIMOUT

def get_lsp_init_config() -> dict:
    try:
        _USER_HOME  = path.expanduser('~')
        _SCRIPT_PTH = path.dirname( path.realpath(__file__) )
        _LSP_INIT_CONFIG = f"{_SCRIPT_PTH}/configs/initialize-params-slim.json"

        with open(_LSP_INIT_CONFIG) as file:
            data = file.read()
            return json.loads(data)
    except Exception as e:
        logger.error( f"LSP Controller: {_LSP_INIT_CONFIG}\n\t\t{repr(e)}" )

    return {}
