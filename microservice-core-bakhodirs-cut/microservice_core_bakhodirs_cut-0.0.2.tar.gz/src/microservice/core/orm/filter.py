import datetime
import operator
from functools import reduce

from sqlalchemy import or_


def generate_clause(condition):
    def handle(field, value):
        clause = getattr(field, condition, None)
        return clause(value)

    return handle


def any_contains(field, value):
    clause = getattr(field, "contains", None)
    conditions = []
    if not isinstance(value, list):
        value = [value]
    for v in value:
        conditions.append(clause([v]))

    return reduce(or_, conditions)


lookups = {
    "eq": operator.eq,
    "neq": operator.ne,
    "lte": operator.le,
    "lt": operator.lt,
    "gte": operator.ge,
    "gt": operator.gt,
    "contains": generate_clause("contains"),
    "any_contains": any_contains,
    "in": generate_clause("in_"),
    "notin": generate_clause("notin_"),
    "like": generate_clause("like"),
    "ilike": generate_clause("ilike"),
}


class FilterField(object):
    def __init__(self, field=None, lookup="eq", cast=lambda x: x, method_name=None):
        assert lookup is not None and isinstance(lookup, str)
        assert field is not None
        self.field = field
        self.lookup = lookup
        self.cast = cast
        self._lookup = lookups.get(lookup, lookups["eq"])
        self.method_name = method_name

    def generate_filter(self, val, method=None):
        if method:
            return method(self.field, val)
        return self._lookup(self.field, self.cast(val))


class BooleanFilterField(FilterField):
    def __init__(self, *args, **kwargs):
        super(BooleanFilterField, self).__init__(*args, **kwargs)

    def generate_filter(self, val: str, method=None):
        val = val.lower() == "true"
        if method:
            return method(self.field, val)
        return self._lookup(self.field, val)


class DateFilterField(FilterField):
    def __init__(self, *args, **kwargs):
        super(DateFilterField, self).__init__(*args, **kwargs)
        self.cast = lambda x: datetime.datetime.fromisoformat(x).date()


class DateTimeFilterField(FilterField):
    def __init__(self, *args, **kwargs):
        super(DateTimeFilterField, self).__init__(*args, **kwargs)
        self.cast = lambda x: datetime.datetime.fromisoformat(x)


class Filter(object):
    def __init__(self):
        self.fields = dict()
        for name, filter_field in self.__class__.__dict__.items():
            if isinstance(filter_field, FilterField):
                self.fields[name] = filter_field

    def get_clauses(self, **kwargs):
        clauses = []
        for name, value in kwargs.items():
            filter_field = self.fields.get(name)
            if not filter_field:
                continue
            prepare = getattr(self, f"prepare_{name}", lambda x: x)
            value = prepare(value)
            method = None
            if filter_field.method_name:
                method = getattr(self, filter_field.method_name, None)
            clauses.append(filter_field.generate_filter(value, method))
        return clauses
