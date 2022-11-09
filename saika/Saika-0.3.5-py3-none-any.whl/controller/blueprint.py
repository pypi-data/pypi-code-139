from typing import Optional, TYPE_CHECKING

from flask import Blueprint

from .base import BaseController

if TYPE_CHECKING:
    from saika.app import SaikaApp


class BlueprintController(BaseController):
    def __init__(self):
        super().__init__()
        self._blueprint = Blueprint(self.name, self.import_name)
        self._functions = []
        self._app = None  # type: Optional[SaikaApp]

    @property
    def blueprint(self):
        return self._blueprint

    @property
    def functions(self):
        return self._functions

    @property
    def app(self):
        return self._app

    def register(self, app):
        super().register()
        self._app = app
        self._register_functions()
        app.register_blueprint(self._blueprint, **self.options)

    def _register_functions(self):
        pass
