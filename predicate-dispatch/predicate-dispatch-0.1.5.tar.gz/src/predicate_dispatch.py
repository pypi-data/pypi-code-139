# Copyright 2015 Juraj Sebin <sebin.juraj@gmail.com>
# Copyright 2022 Dmitriy Pertsev <davaeron@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Predicate dispatch"""

from typing import Any, Callable, Dict, List, Optional, Tuple


ConditionFunction = Callable[[Any], bool]
CodeFunction = Callable[[Any], Any]
CallableList = List[Tuple[ConditionFunction, CodeFunction]]


_conditional_callables: Dict[str, CallableList] = {}
_conditional_callables_defaults: Dict[str, Optional[CodeFunction]] = {}


def _get_qualname(func: CodeFunction) -> str:
    return func.__qualname__


def _add_callable(condition: Optional[ConditionFunction], func: CodeFunction) -> None:
    qual_name: str = _get_qualname(func)
    if condition is not None:
        _conditional_callables.setdefault(qual_name, []).append((condition, func))
    else:
        _conditional_callables_defaults[qual_name] = func


def _resolve_callable(
    func: CodeFunction, *args: Any, **kwargs: Any
) -> Optional[CodeFunction]:
    qual_name: str = _get_qualname(func)
    callable_iterator = (
        cc[1] for cc in _conditional_callables[qual_name] if cc[0](*args, **kwargs)
    )
    return next(
        callable_iterator,
        _conditional_callables_defaults.setdefault(qual_name, None),
    )


def predicate(condition: Optional[ConditionFunction] = None) -> CodeFunction:
    """Predicate decorator function"""

    def wrapper(func: CodeFunction) -> CodeFunction:
        _add_callable(condition, func)

        def wrapped(*args: Any, **kwargs: Any) -> Any:
            resolved_callable: Optional[CodeFunction] = _resolve_callable(
                func, *args, **kwargs
            )
            if resolved_callable is not None:
                return resolved_callable(*args, **kwargs)
            else:
                raise TypeError(f"Predicate for '{_get_qualname(func)}' is not found")

        return wrapped

    return wrapper
