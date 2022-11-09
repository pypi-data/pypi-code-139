# system modules
import collections
import logging
import re
import importlib

# internal modules
from polt.filter import Filter
from polt import utils

# external modules
import numpy as np


logger = logging.getLogger(__name__)


class CalculationFilter(Filter):
    """
    Filter for modifying values with calculations
    """

    @property
    def when_quantity(self):
        """
        Only operate on quantities matching this regular expression

        .. note::

            Set this option from the command-line via
            ``polt add-filter -f calculate -o when-quantity=PATTERN``

        :type: :class:`str` or ``None``
        """
        try:
            self._when_quantity
        except AttributeError:
            self._when_quantity = re.compile(".*")
        return self._when_quantity

    @when_quantity.setter
    def when_quantity(self, new):
        self._when_quantity = re.compile(
            str(new) if new else r".*", flags=re.IGNORECASE
        )

    @property
    def when_unit(self):
        """
        Only operate on units matching this regular expression

        .. note::

            Set this option from the command-line via
            ``polt add-filter -f calculate -o when-unit=PATTERN``

        :type: :class:`str` or ``None``
        """
        try:
            self._when_unit
        except AttributeError:
            self._when_unit = re.compile(".*")
        return self._when_unit

    @when_unit.setter
    def when_unit(self, new):
        self._when_unit = re.compile(
            str(new) if new else r".*", flags=re.IGNORECASE
        )

    @property
    def when_key(self):
        """
        Only operate on keys matching this regular expression

        .. note::

            Set this option from the command-line via
            ``polt add-filter -f calculate -o when-key=PATTERN``

        :type: :class:`str` or ``None``
        """
        try:
            self._when_key
        except AttributeError:
            self._when_key = re.compile(".*")
        return self._when_key

    @when_key.setter
    def when_key(self, new):
        self._when_key = re.compile(
            str(new) if new else r".*", flags=re.IGNORECASE
        )

    @property
    def count(self):
        """
        Operate on this many past values. Defaults to 1.

        .. note::

            Set this option from the command-line via
            ``polt add-filter -f calculate -o count=NUMBER``

        :type: :class:`str` or ``None``
        """
        try:
            self._count
        except AttributeError:
            self._count = 1
        return self._count

    @count.setter
    def count(self, new):
        self._count = max(1, int(new))

    @property
    def new_quantity(self):
        """
        Change the quantity of the newly created data. The strings
        ``{quantity}``, ``{key}``, ``{unit}`` of the current data and
        ``{function}`` are replaced in this string.

        .. note::

            Set this option from the command-line via
            ``polt add-filter -f calculate -o new-quantity='other {quantity}'``

        :type: :class:`str` or ``None``
        """
        try:
            return self._new_quantity
        except AttributeError:
            self._new_quantity = "{function}({quantity})"
        return self._new_quantity

    @new_quantity.setter
    def new_quantity(self, new):
        self._new_quantity = new if new else None

    @property
    def new_unit(self):
        """
        Change the unit of the newly created data. The strings
        ``{quantity}``, ``{key}``, ``{unit}`` of the current data and
        ``{function}`` are replaced in this string.

        .. note::

            Set this option from the command-line via
            ``polt add-filter -f calculate -o new-unit='not {unit} anymore'``

        :type: :class:`str` or ``None``
        """
        try:
            return self._new_unit
        except AttributeError:
            self._new_unit = "{unit}"
        return self._new_unit

    @new_unit.setter
    def new_unit(self, new):
        self._new_unit = new if new else None

    @property
    def new_key(self):
        """
        Change the key of the newly created data. The strings
        ``{quantity}``, ``{key}``, ``{unit}`` of the current data and
        ``{function}`` are replaced in this string.

        .. note::

            Set this option from the command-line via
            ``polt add-filter -f calculate -o new-key='not {key} anymore'``

        :type: :class:`str` or ``None``
        """
        try:
            return self._new_key
        except AttributeError:
            self._new_key = "{key}"
        return self._new_key

    @new_key.setter
    def new_key(self, new):
        self._new_key = new if new else None

    @property
    def function(self):
        """
        .. note::

          Examples:

          .. code-block:: sh

            # running mean over last 10 values
            polt add-filter -f calculate -o function=numpy.mean -o count=10

            # running median over last 10 values
            polt add-filter -f calculate -o function=numpy.median -o count=10

            # scaling a specific quantity and changing the unit
            polt add-filter -f calculate \\
                -o when-quantity='temperature.*celsius' \\
                -o function=lambda x: x + 273.15  \\
                -o new-unit=Kelvin

            # using a function myfunction() in a separate Python file myfile.py
            polt add-filter -f calculate -o function=myfile.myfunction
        """
        try:
            return self._function
        except AttributeError:
            self._function = None
        return self._function

    @function.setter
    def function(self, new):
        """ """
        if m := re.fullmatch(
            r"(?P<modulename>.*?)\.(?P<objectname>[a-z]+)",
            str(new),
            flags=re.IGNORECASE,
        ):
            module = importlib.import_module(m.groupdict()["modulename"])
            self._function = getattr(
                module,
                m.groupdict()["objectname"],
            )
        else:
            try:
                # 😈 Dirty eval() 😈
                func = eval(new)
                if not hasattr(func, "__call__"):
                    raise ValueError()
            except Exception:
                raise ValueError(
                    f"Neither a Python function path like "
                    f"'package.submodule.functionname' "
                    f"nor a function definition: {new!r}"
                )
            self._function = func

    @property
    def cache(self):
        try:
            self._cache
        except AttributeError:
            self._cache = collections.defaultdict(
                lambda: collections.deque([], maxlen=self.count)
            )
        return self._cache

    def update_dataset(self, dataset):
        """
        ...

        Args:
            dataset (dict): the dataset to modify

        Returns:
            dict or None: the modified dataset

        """
        if not self.function:
            return dataset
        data = dataset.get("data", {})
        newdata = {}
        for key, val in data.items():
            logger.debug(f"{key = }, {val = }")
            keyiter = iter(utils.to_tuple(key))
            props = {
                p: next(keyiter, None) for p in ("quantity", "unit", "key")
            }
            regexes = {
                p: getattr(self, f"when_{p}", re.compile(r".*")) for p in props
            }
            matches = {p: regexes[p].search(v or "") for p, v in props.items()}
            if not all(matches.values()):
                continue
            try:
                self.cache[key].extend(val)
            except TypeError:
                self.cache[key].append(val)
            # construct new properties
            newprops = {}
            for p in props:
                template = getattr(self, f"new_{p}", f"{{{p}}}")
                try:
                    newprops[p] = template.format(
                        **dict(
                            **props,
                            function=getattr(
                                self.function,
                                "__name__",
                                f"function-{id(self.function)}",
                            ),
                        )
                    )
                except (ValueError, KeyError) as e:
                    logger.error(
                        f"Couldn't format {template = !r}: "
                        f"{type(e).__name__} {e}"
                    )
                    newprops[p] = template

            cachearray = np.asfarray(
                tuple(map(utils.to_float, self.cache[key]))
            )
            logger.debug(f"{cachearray = }")
            logger.debug(f"{self.function = }")
            try:
                newval = self.function(cachearray)
            except Exception as e:
                logger.error(
                    f"{type(e)} during "
                    f"{getattr(self.function,'__name__',str(self.function))}"
                    f"({cachearray}): {e}"
                )
                continue
            newdata[
                tuple(
                    (
                        newprops[k].format(**props)
                        if isinstance(newprops[k], str)
                        else newprops[k]
                    )
                    for k in ("quantity", "unit", "key")
                )
            ] = newval
        # add new data to dataset
        data.update(newdata)
        return dataset
