# system modules
import logging
import re

# internal modules
from polt.filter import Filter
from polt import utils

# external modules
import numpy as np


logger = logging.getLogger(__name__)


class SelectionFilter(Filter):
    """
    Filter for dropping or keeping only specific data
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
    def action(self):
        """
        What to do with the matched data. Either ``"drop"`` or ``"keep"``
        (default).
        """
        try:
            return self._action
        except AttributeError:
            self._action = "keep"
        return self._action

    @action.setter
    def action(self, new):
        options = ("keep", "drop")
        if new not in options:
            raise ValueError(f"action must be either {options}, not {new}")
        self._action = new

    def update_dataset(self, dataset):
        """
        ...

        Args:
            dataset (dict): the dataset to modify

        Returns:
            dict or None: the modified dataset

        """
        matched = []
        data = dataset.get("data", {})
        for key, val in data.items():
            keyiter = iter(utils.to_tuple(key))
            props = {
                p: next(keyiter, None) for p in ("quantity", "unit", "key")
            }
            regexes = {
                p: getattr(self, f"when_{p}", re.compile(r".*")) for p in props
            }
            matches = {p: regexes[p].search(v or "") for p, v in props.items()}
            if all(matches.values()):
                matched.append(key)
        for k in (
            (set(data) - set(matched)) if self.action == "keep" else matched
        ):
            data.pop(k, None)
        return dataset
