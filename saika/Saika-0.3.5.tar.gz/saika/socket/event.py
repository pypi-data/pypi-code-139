from geventwebsocket.exceptions import WebSocketError
from geventwebsocket.websocket import WebSocket, MSG_SOCKET_DEAD

from .controller import SocketController


class EventSocketController(SocketController):
    def handle(self, socket: WebSocket):
        self.socket = socket
        self.on_connect()
        while not socket.closed:
            try:
                data = self.receive()
                if not data:
                    continue
                if isinstance(data, dict):
                    event = data.pop('event')
                    if not self.callback_before_event(event):
                        continue
                    event_attr = f'on_{event}'
                    if event_attr in self.attrs:
                        kwargs = data.pop('data', {})
                        getattr(self, event_attr)(**kwargs)
                        continue
                self.on_message(data)
            except WebSocketError as e:
                if MSG_SOCKET_DEAD in e.args:
                    break
                self.on_error(e)
            except Exception as e:
                self.on_error(e)
        self.on_disconnect()

    def emit(self, event: str, data=None):
        self.send(dict(event=event, data=data))

    def disconnect(self, *args, **kwargs):
        self.socket.close(*args, **kwargs)

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_message(self, data):
        pass

    def on_error(self, e: Exception):
        raise e

    def callback_before_event(self, event):
        return True
