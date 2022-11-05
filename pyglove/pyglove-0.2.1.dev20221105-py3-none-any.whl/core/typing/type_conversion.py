# Copyright 2022 The PyGlove Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Automatic type conversions."""

import calendar
import datetime
from typing import Any, Callable, Optional, Tuple, Type, Union

from pyglove.core import object_utils


class _TypeConverterRegistry:
  """Type converter registry."""

  def __init__(self):
    """Constructor."""
    self._converter_list = []
    self._json_value_types = set(
        [int, float, bool, type(None), list, tuple, dict, str])

  def register(
      self,
      src: Union[Type[Any], Tuple[Type[Any], ...]],
      dest: Union[Type[Any], Tuple[Type[Any], ...]],
      convert_fn: Callable[[Any], Any]) -> None:  # pyformat: disable pylint: disable=line-too-long
    """Register a converter from src type to dest type."""
    if (not isinstance(src, (tuple, type)) or
        not isinstance(dest, (tuple, type))):
      raise TypeError('Argument \'src\' and \'dest\' must be a type or '
                      'tuple of types.')
    if isinstance(dest, tuple):
      json_value_convertible = False
      for d in dest:
        for dest_type in self._json_value_types:
          if issubclass(d, dest_type):
            json_value_convertible = True
            break
        if json_value_convertible:
          break
    else:
      json_value_convertible = False
      for dest_type in self._json_value_types:
        if issubclass(dest, dest_type):
          json_value_convertible = True
          break
    self._converter_list.append((src, dest, convert_fn, json_value_convertible))

  def get_converter(
      self, src: Type[Any], dest: Type[Any]) -> Optional[Callable[[Any], Any]]:
    """Get converter from source type to destination type."""
    # TODO(daiyip): Right now we don't see the need of a large number of
    # converters, thus its affordable to iterate the list.
    # We may consider more efficient way to do lookup in future.
    # NOTE(daiyip): We do reverse lookup since usually subclass converter
    # is register after base class.
    for src_type, dest_type, converter, _ in reversed(self._converter_list):
      if issubclass(src, src_type) and issubclass(dest, dest_type):
        return converter
    return None

  def get_json_value_converter(
      self, src: Type[Any]) -> Optional[Callable[[Any], Any]]:
    """Get converter from source type to a JSON simple type."""
    for src_type, _, converter, json_value_convertible in reversed(
        self._converter_list):
      if issubclass(src, src_type) and json_value_convertible:
        return converter
    return None


_TYPE_CONVERTER_REGISTRY = _TypeConverterRegistry()


def get_converter(
    src: Type[Any], dest: Type[Any]
) -> Optional[Callable[[Any], Any]]:
  """Get converter from source type to destination type."""
  return _TYPE_CONVERTER_REGISTRY.get_converter(src, dest)


def get_first_applicable_converter(
    src_type: Type[Any],
    dest_type_or_types: Union[Type[Any], Tuple[Type[Any], ...]]):
  """Get first applicable converter."""
  if isinstance(dest_type_or_types, tuple):
    dest_types = list(dest_type_or_types)
  else:
    dest_types = [dest_type_or_types]
  for dest_type in dest_types:
    converter = get_converter(src_type, dest_type)
    if converter is not None:
      return converter
  return None


def get_json_value_converter(src: Type[Any]) -> Optional[Callable[[Any], Any]]:
  """Get converter from source type to a JSON simple type."""
  return _TYPE_CONVERTER_REGISTRY.get_json_value_converter(src)


def register_converter(
    src_type: Union[Type[Any], Tuple[Type[Any], ...]],
    dest_type: Union[Type[Any], Tuple[Type[Any], ...]],
    convert_fn: Callable[[Any], Any]) -> None:
  """Register converter from source type to destination type.

  Examples::

    # Add converter from int to float.
    pg.typing.register_converter(int, float, float)

    assert pg.typing.Float().apply(1) is 1.0

    # Add converter from a dict to class A.
    def from_dict(d):
      return A(**d)

    assert isinstance(pg.typing.Object(A).apply({'x': 1, 'y': 2}), A)

  Args:
      src_type: Source value type.
      dest_type: Target value type.
      convert_fn: Function that performs the conversion, in signature
        (src_type) -> dest_type.
  """
  _TYPE_CONVERTER_REGISTRY.register(src_type, dest_type, convert_fn)


def _register_builtin_converters():
  """Register built-in converters."""
  # int <=> datetime.datetime.
  register_converter(int, datetime.datetime, datetime.datetime.utcfromtimestamp)
  register_converter(datetime.datetime, int,
                     lambda x: calendar.timegm(x.timetuple()))

  # string <=> KeyPath.
  register_converter(str, object_utils.KeyPath,
                     object_utils.KeyPath.parse)
  register_converter(object_utils.KeyPath, str, lambda x: x.path)


_register_builtin_converters()

