from json import JSONDecodeError

from geventwebsocket.websocket import WebSocket

from saika import hard_code, common
from saika.context import Context
from saika.controller import BlueprintController, BaseController
from saika.meta_table import MetaTable


class SocketController(BlueprintController):
    def register(self, socket):
        BaseController.register(self)
        self._register_functions()
        socket.register_blueprint(self.blueprint, **self.options)

    def _register_functions(self):
        for f in self.methods:
            _f = f
            f = getattr(f, '__func__', f)

            meta = MetaTable.all(f)
            if meta is not None:
                self._blueprint.add_url_rule(meta[hard_code.MK_RULE_STR], None, _f)
                self._functions.append(_f)

    @property
    def socket(self):
        socket = Context.g_get(hard_code.GK_SOCKET)  # type: WebSocket
        return socket

    @socket.setter
    def socket(self, value):
        Context.g_set(hard_code.GK_SOCKET, value)

    def send(self, data: dict):
        if self.socket.closed:
            return

        self.socket.send(common.to_json(common.obj_standard(data, True, True, True)))

    def receive(self):
        if self.socket.closed:
            return

        data_str = None
        try:
            data_str = self.socket.receive()
            if data_str:
                return common.from_json(data_str)  # type: dict
        except JSONDecodeError:
            return data_str
