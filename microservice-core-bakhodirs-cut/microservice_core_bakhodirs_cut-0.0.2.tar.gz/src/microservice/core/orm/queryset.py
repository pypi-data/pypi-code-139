import typing
from copy import deepcopy

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.sql import operators as op
from sqlalchemy.sql.elements import Label

from src.microservice.core.database import db

db_funcs = (
    db.func.coalesce,
    db.func.max,
    db.func.min,
    db.func.sum,
    db.func.now,
    db.func.concat,
    db.func.char_length,
    db.func.random,
    db.func.count,
    db.func.current_date,
    db.func.current_time,
    db.func.current_timestamp,
    db.func.current_user,
    db.func.localtime,
    db.func.localtimestamp,
    db.func.session_user,
    db.func.sysdate,
    db.func.user,
    db.func.array_agg,
    db.func.OrderedSetAgg,
    db.func.mode,
    db.func.percentile_cont,
    db.func.percentile_disc,
    db.func.rank,
    db.func.dense_rank,
    db.func.percent_rank,
    db.func.cume_dist,
    db.func.cube,
    db.func.rollup,
    db.func.grouping_sets,
)

reverse_ops = {
    op.eq: op.ne,
    op.lt: op.gt,
    op.gt: op.lt,
    op.in_op: op.notin_op,
    op.notin_op: op.in_op,
}


class Queryset(object):
    def __init__(self, klass):
        self.__alias = None
        self.page = None
        self.limit = None
        self.orderings = []
        self.klass = klass
        self.default_filters = dict()
        self.and_filters = []
        self.exclude_filters = []
        self.functions = []
        self.result_fields = None
        self.distinct_fields = []
        self.annotate_fields = dict()
        self.group_by_fields = []

        self.alias = list()
        self.join_conditions = list()
        self.loaders = dict()
        self.has_soft_delete = "is_deleted" in klass._column_name_map
        self.select_for_update = False
        self.is_scalar = False

    def fields(self, *args):
        qs = deepcopy(self)
        result_fields = dict()
        for arg in args:
            if isinstance(arg, str):
                field_name = arg
                field_value = sa.column(arg)
                if field_name in self.result_fields:
                    field_value = self.result_fields[field_name]
            elif isinstance(arg, (db.Column, sa.sql.elements.Label)):
                field_name = arg.name
                field_value = arg
            else:
                continue
            result_fields[field_name] = field_value
        qs.result_fields = result_fields
        return qs

    def distinct(self, *args):
        qs = deepcopy(self)
        qs.distinct_fields = args
        return qs

    def group_by(self, *args):
        qs = deepcopy(self)
        group_by = []
        for arg in args:
            if isinstance(arg, str):
                group_by.append(sa.column(arg))
            else:
                group_by.append(arg)
        qs.group_by_fields = group_by
        return qs

    def for_update(self, select_for_update=True):
        qs = deepcopy(self)
        qs.select_for_update = select_for_update
        return qs

    def annotate(self, **kwargs):
        qs = deepcopy(self)
        for key, (func, type_) in kwargs.items():
            qs.annotate_fields.update({key: func.label(key)})
            qs.loaders[key] = db.Column(key, type_)
        return qs

    def subquery(self, **kwargs):
        qs = deepcopy(self)
        for key, subquery in kwargs.items():
            qs.result_fields[key] = subquery.alias(key)
        return qs

    def filter(self, *args):
        qs = deepcopy(self)
        if args:
            qs.and_filters += list(args)
        return qs

    def exclude(self, *args):
        qs = deepcopy(self)
        for query in args:
            query.operator = reverse_ops[query.operator]
            qs.exclude_filters.append(query)
        return qs

    def paginate(self, page, limit):
        if not page or not limit:
            return self
        assert page > 0 and limit > 0, "Paginating values should be greater than zero"
        qs = deepcopy(self)
        qs.page, qs.limit = page, limit
        return qs

    def order_by(self, *args):
        qs = deepcopy(self)
        if not args:
            qs.orderings = []
            return qs
        for value in args:
            if isinstance(value, str):
                if len(value) and value[0] == "-":
                    field = getattr(self.klass, value[1:], None)
                    assert (
                        field is not None
                    ), f"Class {self.klass} does not have field {value[1:]}"
                    qs.orderings.append(field.desc())
                else:
                    field = getattr(self.klass, value, None)
                    assert (
                        field is not None
                    ), f"Class {self.klass} does not have field {value[1:]}"
                    qs.orderings.append(field.asc())
            else:
                qs.orderings.append(value)
        return qs

    def join(self, alias, condition, under_key=None):
        qs = deepcopy(self)
        qs.alias.append(alias)
        qs.join_conditions.append((alias, condition))
        if under_key:
            qs.loaders[under_key] = alias
        return qs

    def _generate_query(self):
        qs = db

        fields = []
        if self.functions:
            fields += self.functions
        elif self.result_fields is not None:
            fields += list(self.result_fields.values())
        elif self.alias:
            fields += [self.klass, *self.alias]
        else:
            fields += [self.klass]

        if self.annotate_fields and not self.is_scalar:
            fields += list(self.annotate_fields.values())

        if self.distinct_fields:
            qs = qs.select(fields, distinct=self.distinct_fields)
        else:
            qs = qs.select(fields)

        if self.group_by_fields:
            for group in self.group_by_fields:
                qs = qs.group_by(group)
        if self.join_conditions:
            from_ = self.klass
            for condition in self.join_conditions:
                from_ = from_.outerjoin(*condition)
            qs = qs.select_from(from_)
        if self.and_filters:
            qs = qs.where(sa.and_(*self.and_filters))
        if self.exclude_filters:
            qs = qs.where(sa.and_(*self.exclude_filters))
        if self.orderings:
            qs = qs.order_by(*self.orderings)
        if self.page and self.limit:
            qs = qs.limit(self.limit).offset((self.page - 1) * self.limit)
        elif self.limit:
            qs = qs.limit(self.limit)

        if self.select_for_update:
            qs = qs.with_for_update()
        return qs

    def _generate_exists_query(self):
        qs = db.exists()

        if self.group_by_fields:
            for group in self.group_by_fields:
                qs = qs.group_by(group)
        if self.join_conditions:
            from_ = self.klass
            for condition in self.join_conditions:
                from_ = from_.outerjoin(*condition)
            qs = qs.select_from(from_)
        if self.and_filters:
            qs = qs.where(sa.and_(*self.and_filters))
        if self.exclude_filters:
            qs = qs.where(sa.and_(*self.exclude_filters))
        if self.orderings:
            qs = qs.order_by(*self.orderings)
        if self.page and self.limit:
            qs = qs.limit(self.limit).offset((self.page - 1) * self.limit)
        elif self.limit:
            qs = qs.limit(self.limit)
        return qs

    def _generate_update_query(self):
        qs = db
        qs = qs.update(self.klass)
        if self.and_filters:
            qs = qs.where(sa.and_(*self.and_filters))
        if self.exclude_filters:
            qs = qs.where(sa.and_(*self.exclude_filters))
        return qs

    def _generate_delete_query(self, is_hard):
        qs = db
        delete_function = qs.delete if is_hard else qs.update
        qs = delete_function(self.klass)

        if self.and_filters:
            qs = qs.where(sa.and_(*self.and_filters))
        if self.exclude_filters:
            qs = qs.where(sa.and_(*self.exclude_filters))

        return qs

    async def count(self, field_name="id"):
        qs = deepcopy(self)
        qs.is_scalar = True
        field = getattr(self.klass, field_name, None)
        assert (
            field is not None
        ), f"Field {field_name} in {str(self.klass)} does not exits"
        qs.functions.append(db.func.count(field))
        qs = qs._generate_query()
        return await qs.gino.scalar()

    def _all(self):
        qs = self._generate_query()
        qs = qs.gino
        if self.loaders:
            qs = qs.load(self.klass.load(**self.loaders))
        else:
            qs = qs.load(self.klass)

        return qs

    def all(self):
        qs = self._all()
        return qs.all()

    def _exists(self):
        qs = self._generate_exists_query()
        return qs

    def exists(self):
        return db.scalar(self._exists().select())

    def exists_query(self):
        return self._exists()

    def get(self, *args):
        qs = self.filter(*args)
        qs = qs._all()
        return qs.first()

    async def create(self, **kwargs):
        obj = await self.klass.create(**kwargs)
        if not self.loaders:
            return obj
        qs = self.filter(self.klass.id == obj.id)
        return await qs.get()

    async def update_or_create(self, key_, **values):
        if not isinstance(key_, (list, tuple)):
            key_ = [key_]

        for key__ in key_:
            assert (
                getattr(self.klass, key__, None) is not None
            ), "Indicated field does not exist in model"
            assert key__ in values, "Define key field in values positional arguments"
        key_fields = []

        for key__ in key_:
            key_fields.append(getattr(self.klass, key__))

        qs = pg_insert(self.klass.__table__).values(**values)
        qs = qs.on_conflict_do_update(index_elements=[*key_fields], set_=values)
        qs = qs.returning(self.klass.__table__)
        results = await qs.gino.load(self.klass).all()
        for key_field in key_fields:
            if key_field.autoincrement and type(key_field.type) == db.Integer:
                query = f"""
                    SELECT SETVAL('{self.klass.__tablename__}_id_seq',
                         (SELECT COALESCE(MAX(id) + 1, 1) FROM "{self.klass.__tablename__}"), false)
                """
                await db.status(query)
        return results[0]

    async def create_or_update(
        self, key_, create_values: dict, update_values: dict
    ) -> typing.Tuple[object, bool]:
        if not isinstance(key_, (list, tuple)):
            key_ = [key_]

        exists_qs = self.__class__(self.klass).filter(self.klass.is_deleted == False)

        for key__ in key_:
            assert (
                getattr(self.klass, key__, None) is not None
            ), "Indicated field does not exist in model"
            assert (
                key__ in create_values
            ), "Define key field in create values positional arguments"
            assert (
                key__ in update_values
            ), "Define key field in update values positional arguments"
            exists_qs = exists_qs.filter(
                getattr(self.klass, key__, None) == create_values[key__]
            )
        key_fields = []

        for key__ in key_:
            key_fields.append(getattr(self.klass, key__))

        is_exist = await exists_qs.exists()

        qs = pg_insert(self.klass.__table__).values(**create_values)
        qs = qs.on_conflict_do_update(index_elements=[*key_], set_=update_values)
        qs = qs.returning(self.klass.__table__)
        results = await qs.gino.load(self.klass).all()
        return results[0], not is_exist

    def __deepcopy__(self, memodict={}):
        obj_copy = self.__class__(self.klass)
        obj_copy.page = deepcopy(self.page)
        obj_copy.limit = deepcopy(self.limit)
        obj_copy.orderings = list(self.orderings)
        obj_copy.klass = self.klass
        obj_copy.default_filters = list(self.default_filters)
        obj_copy.and_filters = list(self.and_filters)
        obj_copy.exclude_filters = list(self.exclude_filters)
        obj_copy.functions = list(self.functions)
        obj_copy.result_fields = dict(self.result_fields) if self.result_fields is not None else None
        obj_copy.distinct_fields = tuple(self.distinct_fields)
        obj_copy.annotate_fields = dict(self.annotate_fields)
        obj_copy.alias = list(self.alias)
        obj_copy.join_conditions = list(self.join_conditions)
        obj_copy.loaders = dict(self.loaders)
        obj_copy.group_by_fields = list(self.group_by_fields)
        obj_copy.has_soft_delete = bool(self.has_soft_delete)
        obj_copy.select_for_update = bool(self.select_for_update)
        obj_copy.is_scalar = bool(self.is_scalar)
        return obj_copy

    async def bulk_create(self, data: list):
        """
        Note: given each piece of data should contain similar key name(order) and count of variables
            Success:
            [
                {
                    "id": 1, "firstname": "Tom", "lastname": "Isaak",
                },
                {
                    "id": 2, "firstname": "Susan", "lastname": "Mariarti",
                },
            ]
            Fails:
            [
                {
                    "id": 1, "firstname": "Tom",
                },
                {
                    "id": 2, "lastname": "Mariarti",
                },
            ]
        """
        try:
            qs = sa.insert(self.klass.__table__)
            qs = qs.values(data)
            qs = qs.returning(self.klass.__table__)
            if data:
                results = await qs.gino.load(self.klass).all()
            else:
                results = []
            return None, results
        except Exception as e:
            print(
                "~~~Bulk create begin~~~",
                str(e),
                self.klass,
                data,
                "~~~Bulk create end~~~",
            )
            return str(e), []

    @staticmethod
    async def raw_query(query: str, filters=None, column_order=None, **__):
        """

        :param query: String query  select *, annotation as col_name from table where id = :id
        :param filters: {'id': 1}
        :param column_order: ['col1_name', 'col2_name', ...]
        :param __:
        :return:
        """
        if column_order is None:
            column_order = list()
        if filters is None:
            filters = dict()

        results = await db.all(db.text(query), **filters)

        objs = []

        if results and not column_order:
            column_order = results[0]._keymap.keys()

        for result in results:
            objs.append(dict(zip(column_order, result)))

        return objs

    @staticmethod
    async def execute(query, columns, **filters):
        if filters:
            status, results = await db.status(db.text(query), filters)
        else:
            status, results = await db.status(query)
        results = map(lambda result: dict(zip(columns, result)), results)
        return results

    def _update(self, **kwargs):
        update_qs = self._generate_update_query()
        update_qs = update_qs.values(**kwargs)
        update_qs = update_qs.returning(*self.klass.query.columns)
        update_qs = update_qs.gino.load(self.klass)
        return update_qs

    def update(self, **kwargs):
        qs = self._update(**kwargs)
        return qs.all()

    def _delete(self, is_hard):
        delete_qs = self._generate_delete_query(is_hard)
        if not is_hard:
            delete_qs = delete_qs.values(is_deleted=True)
        return delete_qs

    def delete(self, is_hard=False):
        if not is_hard and not self.has_soft_delete:
            raise ValueError("Model does not have soft delete(is_delete boolean field)")
        return self._delete(is_hard).gino.status()

    @property
    def query(self):
        return self._generate_query()

    @property
    def text(self):
        return self.query.compile(
            compile_kwargs=dict(literal_binds=True), dialect=postgresql.dialect()
        )

    def __str__(self):
        return self.query
