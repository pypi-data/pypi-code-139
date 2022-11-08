from typing import List, Tuple
import sys

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points, EntryPoint  # type: ignore
else:
    from importlib.metadata import entry_points, EntryPoint  # type: ignore

from dependency_injector import providers


class PluginsFactory(providers.Provider):

    __slots__ = ("_factory", "_base_class")

    def __init__(self, base_class, *args, **kwargs):
        self._base_class = base_class
        self._factory = providers.Factory(self._get_provided_type(), *args, **kwargs)
        super().__init__()

    def _get_provided_type(self):
        plugins = self._collect_plugins()
        return self._create_type(plugins)

    def _collect_plugins(self) -> Tuple[type]:
        plugins = []
        for entrypoints_group, entrypoints in entry_points().items():
            if self._should_add(entrypoints_group):
                plugins.extend(self._load_plugins(entrypoints))
        return tuple(plugins)

    def _should_add(self, entrypoints_group_name: str) -> bool:
        return self._base_class.PLUGINS_GROUP_NAME.startswith(entrypoints_group_name)

    def _load_plugins(self, group_entrypoints: List[EntryPoint]) -> List[type]:
        class_plugins = []
        for entrypoint in group_entrypoints:
            class_plugins.append(entrypoint.load())
        return class_plugins

    def _create_type(self, plugins: Tuple[type]) -> type:
        if len(plugins) > 0:
            return type(self._base_class.__name__, plugins, {"PLUGINS_GROUP_NAME": self._base_class.PLUGINS_GROUP_NAME})
        else:
            return self._base_class

    def __deepcopy__(self, memo):
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        copied = self.__class__(
            self._factory.provides,
            *providers.deepcopy(self._factory.args, memo),
            **providers.deepcopy(self._factory.kwargs, memo),
        )
        self._copy_overridings(copied, memo)

        return copied

    @property
    def related(self):
        """Return related providers generator."""
        yield from [self._factory]
        yield from super().related

    def _provide(self, args, kwargs):
        return self._factory(*args, **kwargs)
