import typing
import uuid
from copy import deepcopy
from datetime import datetime, date, time
from datetime import timedelta

from asyncpg.pgproto import pgproto
from sqlalchemy.dialects import postgresql

from src.core.database import db
from src.core.orm.queryset import Queryset


class Model(db.Model):
    __tablename__ = None

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(("id", self.id))

    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        assert self.__tablename__, "Table name is not defined"

    @classmethod
    def objects(cls, alias=None) -> Queryset:
        if alias:
            return Queryset(alias).filter(alias.is_deleted == False)
        return Queryset(cls).filter(cls.is_deleted == False)

    @classmethod
    def raw_objects(cls) -> Queryset:
        return Queryset(cls)

    @classmethod
    def get_fields(cls):
        return [
            (field, getattr(cls, field))
            for field, db_field, in cls._column_name_map.items()
        ]

    async def delete(self):
        await self.update(is_deleted=True).apply()

    async def save(self, **kwargs):
        kwargs.update(self.__values__)
        kwargs["updated_at"] = datetime.now()
        await self.update(**kwargs).apply()

    @classmethod
    def safe_update(cls, **kwargs):
        return cls.update.values(**kwargs).where(cls.is_deleted == False)

    @classmethod
    def safe_delete(cls):
        qs = cls.update.values(is_deleted=True)
        return qs.where(cls.is_deleted == False)

    @property
    def values(self):
        data = self.raw_values
        data.update(**_get_values(self.__dict__))
        return data

    @property
    def raw_values(self):
        data = deepcopy(self.__values__)
        caster = {
            datetime: lambda x: datetime.isoformat(x),
            date: lambda x: date.isoformat(x),
            time: lambda x: time.isoformat(x),
            pgproto.UUID: str,
            postgresql.UUID: str,
            uuid.UUID: str,
            timedelta: lambda x: int(timedelta.total_seconds(x)),
        }
        for k, v in data.items():
            cast = caster.get(type(v), lambda x: x)
            data[k] = cast(v)
        return data

    @property
    def table_name(self):
        return self.__tablename__


class BaseModel(Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_deleted = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), default=datetime.now, index=True)
    updated_at = db.Column(db.DateTime(), default=datetime.now, index=True)

    _primary_key_fields = []

    def __init__(self, *args, **kwargs):
        self._primary_key_fields = self._get_primary_key_fields()
        super(BaseModel, self).__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__} object with id {self.id}"

    def __repr__(self):
        return f"{self.__class__.__name__} object with id {self.id}"

    @classmethod
    def _get_primary_key_fields(cls):
        fields = cls.get_fields()
        primary_key_fields: typing.List[str] = []
        for field_name, field in fields:
            if field.primary_key:
                primary_key_fields.append(field_name)
        return primary_key_fields

    def __get_primary_value(self):
        for field in self._primary_key_fields:
            if getattr(self, field, None):
                return True
        return False

    async def save(self, **kwargs):
        kwargs.update(self.__values__)
        kwargs["updated_at"] = datetime.now()
        if self.__get_primary_value():
            await self.update(**kwargs).apply()
        else:
            new_object = await self.__class__.objects().create(**kwargs)
            self.id = new_object.id


class AnnotateModel(db.Model):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self._values = kwargs

    @property
    def values(self):
        return self._values


def _get_values(data: dict):
    new_data = dict()
    for key, value in data.items():
        if isinstance(value, db.Model):
            new_data[key] = value.values
        elif isinstance(value, (list, tuple)):
            new_data[key] = [v.values if isinstance(v, db.Model) else v for v in value]
        elif isinstance(value, (int, float, str)):
            new_data[key] = value
        elif isinstance(value, uuid.UUID):
            new_data[key] = str(value)
        elif isinstance(value, dict) and "__" not in key:
            new_data[key] = _get_values(value)
    return new_data
