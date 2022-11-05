from ydb import PrimitiveType
# import uuid
import shortuuid
import json
import copy

shortuuid.set_alphabet("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")


class Field:
    title = 'String'

    def __init__(self, pk=False):
        self.pk = pk
        self.changed = False

    def __eq__(self, other):
        # ==
        return '=', self, other

    def __ne__(self, other):
        # !=
        return '!=', self, other

    def __lt__(self, other):
        # <
        return '<', self, other

    def __le__(self, other):
        # <=
        return '<=', self, other

    def __gt__(self, other):
        # >
        return '>', self, other

    def __ge__(self, other):
        # >=
        return '>=', self, other

    def __str__(self):
        if hasattr(self, 'value'):
            return str(self.value)
        return 'None'

    def _init_(self, table, name):
        self.table = table
        self.name = name

    @property
    def need_update(self):
        if self.pk or (hasattr(self, 'value') and self.changed):
            return True

    @property
    def to_save(self):
        return self.value

    def copy(self):
        obj = copy.copy(self)
        return obj

    def set_value(self, value):
        self.value = value


class Utf8(Field):
    title = 'Utf8'
    ydb_type = PrimitiveType.Utf8


class Uuid(Utf8):
    @staticmethod
    def new():
        return shortuuid.uuid()

    def __getattr__(self, item):
        if item == 'value' and self.pk:
            value = self.new()
            self.value = value
            self.changed = True
            return self.new()
        else:
            raise AttributeError(f"{self.__class__.__name__} object has no attribute {item}")


class Int64(Field):
    title = 'Int64'
    ydb_type = PrimitiveType.Int64


class Uint64(Field):
    title = 'Uint64'
    ydb_type = PrimitiveType.Uint64


class Bool(Field):
    title = 'Bool'
    ydb_type = PrimitiveType.Bool


class Datetime(Field):
    title = 'Bool'
    ydb_type = PrimitiveType.Datetime


class Json(Field):
    title = 'Json'
    ydb_type = PrimitiveType.Json

    def set_item(self, d):
        class CheckDict(dict):
            def __setitem__(self_, key, value):
                if value != self_.get(key):
                    self.changed = True
                # print(key, value, self_[key])
                dict.__setitem__(self_, key, value)

        dc = CheckDict()
        dc.update(d)
        return dc

    def __getattribute__(self, item):
        field = object.__getattribute__(self, item)
        if item == 'value':
            if isinstance(field, dict):
                return field
            if field:
                value = json.loads(field, object_hook=self.set_item)
            else:
                value = json.loads('{}', object_hook=self.set_item)
            self.value = value
            return value
        return field

    def __str__(self):
        if hasattr(self, 'value'):
            try:
                value = json.loads(self.value)
            except:
                value = self.value
        else:
            value = ''
        return str(value)

    @property
    def to_save(self):
        value = object.__getattribute__(self, 'value')
        if isinstance(self.value, dict):
            return json.dumps(value)
        return value
