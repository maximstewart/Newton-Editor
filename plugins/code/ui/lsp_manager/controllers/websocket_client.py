# Python imports
import json
import threading

# Lib imports

# Application imports
from ..libs import websocket 



class WebsocketClient:
    def __init__(self):
        self.ws         = None
        self._socket    = None
        self._connected = threading.Event()


    def set_socket(self, socket: str):
        self._socket = socket

    def unset_socket(self):
        self._socket = None

    def send(self, message: str):
        self.ws.send(message)

    def on_message(self, ws, message: dict):
        self.respond(message)

    def on_error(self, ws, error: str):
        logger.debug(f"WS Error:  {error}")

    def on_close(self, ws, close_status_code: int, close_msg: str):
        logger.debug("WS Closed...")

    def on_open(self, ws):
        self._connected.set()
        logger.debug("WS opened connection...")

    def wait_for_connection(self, timeout: float = 5.0) -> bool:
        return self._connected.wait(timeout)

    def set_callback(self, callback: object):
        self.respond = callback

    def close_client(self):
        self.ws.close()

    @daemon_threaded
    def start_client(self):
        if not self._socket:
            raise Exception("Socket address isn't set so cannot start WebsocketClient listener...")

        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self._socket,
                                  on_open    = self.on_open,
                                  on_message = self.on_message,
                                  on_error   = self.on_error,
                                  on_close   = self.on_close)

        self.ws.run_forever(reconnect = 0.5)