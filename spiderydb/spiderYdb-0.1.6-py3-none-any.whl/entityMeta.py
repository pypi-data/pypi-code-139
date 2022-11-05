from .fields import Field
from .query import Query


class EntityMeta(type):

    def __new__(mcs, name, bases, cls_dict):
        if 'Entity' in globals():
            if '__slots__' in cls_dict:
                raise (TypeError, 'Entity classes cannot contain __slots__ variable')
            cls_dict['__slots__'] = ()
        return super(EntityMeta, mcs).__new__(mcs, name, bases, cls_dict)

    def __init__(cls, name, bases, cls_dict):
        super(EntityMeta, cls).__init__(name, bases, cls_dict)
        cls._database_ = None
        if name == 'Entity':
            return
        if hasattr(cls, '__tablename__'):
            cls.table_name = cls.__tablename__
        else:
            cls.table_name = cls.__name__.lower()
        databases = set()
        for base_class in bases:
            if isinstance(base_class, EntityMeta):
                database = base_class._database_
                if database is None:
                    raise (Exception, 'Base Entity does not belong to any database')
                databases.add(database)
        if not databases:
            assert False  # pragma: no cover
        elif len(databases) > 1:
            raise (Exception, 'With multiple inheritance of entities, all entities must belong to the same database')
        database = databases.pop()

        if cls.__name__ in database.entities:
            raise (Exception, 'Entity %s already exists' % cls.__name__)
        assert cls.__name__ not in database.__dict__

        if database.schema is not None:
            raise (Exception,
            'Cannot define entity %r: database mapping has already been generated' % cls.__name__)

        cls._database_ = database

        new_attrs = []
        cls.attrs_dict = {}
        for name, attr in list(cls.__dict__.items()):
            if not isinstance(attr, Field):
                continue
            attr._init_(cls, name)
            new_attrs.append(attr)
            cls.attrs_dict[name] = attr
        cls.attrs = new_attrs

    def _query_from_args_(cls, args, kwargs):
        return Query(cls, args, kwargs).get()

    def get(cls, *args, **kwargs):
        return cls._query_from_args_(args, kwargs)

    def _select_all(cls, args, kwargs):
        return Query(cls, args, kwargs).select()

    def select(cls, *args, **kwargs):
        query = cls._select_all(args, kwargs)
        return query

    def _delete(cls, args, kwargs):
        return Query(cls, args, kwargs).delete()

    def delete(cls, *args, **kwargs):
        query = cls._delete(args, kwargs)
        return query

    def create_table(cls):
        fields, primary_keys = cls.get_fields()
        if not primary_keys:
            raise (Exception, 'no primary key')
        cls._database_.create_table(cls.table_name, fields, primary_keys)

    def get_fields(cls):
        primary_keys = []
        fields = []
        for attr in cls.attrs:
            fields.append((attr.name, attr.ydb_type))
            if attr.pk:
                primary_keys.append(attr.name)
        return fields, primary_keys

    def update_columns(cls):
        fields, primary_keys = cls.get_fields()
        cls._database_.update_columns(cls.table_name, fields, primary_keys)
