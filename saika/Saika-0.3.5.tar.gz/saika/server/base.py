from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from saika import SaikaApp


class BaseServer:
    def __init__(self, app):
        self.app = app  # type: SaikaApp

    def run(self, host, port, debug, use_reloader, ssl_crt, ssl_key, **kwargs):
        pass
