from functools import cached_property

from saika import hard_code, common
from saika.meta_table import MetaTable


class BaseController:
    def __init__(self):
        pass

    @cached_property
    def name(self):
        return common.get_lower_name(
            self.__class__.__name__.replace('Controller', '')
        )

    @cached_property
    def import_name(self):
        return self.__class__.__module__

    @property
    def options(self):
        options = MetaTable.get(self.__class__, hard_code.MK_OPTIONS, {})  # type: dict
        return options

    @cached_property
    def attrs(self):
        keys = []
        for parent_cls in self.__class__.__mro__[0:-2]:
            for k, v in parent_cls.__dict__.items():
                if not k.startswith('_') and not isinstance(v, property):
                    keys.append(k)

        return {k: getattr(self, k) for k in set(keys)}

    @cached_property
    def methods(self):
        return [method for method in self.attrs.values() if callable(method)]

    def register(self, *args, **kwargs):
        self.callback_before_register()

    def callback_before_register(self):
        pass
