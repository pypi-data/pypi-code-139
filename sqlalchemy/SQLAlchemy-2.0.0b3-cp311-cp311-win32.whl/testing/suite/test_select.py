# mypy: ignore-errors

import collections.abc as collections_abc
import itertools

from .. import AssertsCompiledSQL
from .. import AssertsExecutionResults
from .. import config
from .. import fixtures
from ..assertions import assert_raises
from ..assertions import eq_
from ..assertions import in_
from ..assertsql import CursorSQL
from ..schema import Column
from ..schema import Table
from ... import bindparam
from ... import case
from ... import column
from ... import Computed
from ... import exists
from ... import false
from ... import ForeignKey
from ... import func
from ... import Identity
from ... import Integer
from ... import literal
from ... import literal_column
from ... import null
from ... import select
from ... import String
from ... import table
from ... import testing
from ... import text
from ... import true
from ... import tuple_
from ... import TupleType
from ... import union
from ... import values
from ...exc import DatabaseError
from ...exc import ProgrammingError


class CollateTest(fixtures.TablesTest):
    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "some_table",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("data", String(100)),
        )

    @classmethod
    def insert_data(cls, connection):
        connection.execute(
            cls.tables.some_table.insert(),
            [
                {"id": 1, "data": "collate data1"},
                {"id": 2, "data": "collate data2"},
            ],
        )

    def _assert_result(self, select, result):
        with config.db.connect() as conn:
            eq_(conn.execute(select).fetchall(), result)

    @testing.requires.order_by_collation
    def test_collate_order_by(self):
        collation = testing.requires.get_order_by_collation(testing.config)

        self._assert_result(
            select(self.tables.some_table).order_by(
                self.tables.some_table.c.data.collate(collation).asc()
            ),
            [(1, "collate data1"), (2, "collate data2")],
        )


class OrderByLabelTest(fixtures.TablesTest):
    """Test the dialect sends appropriate ORDER BY expressions when
    labels are used.

    This essentially exercises the "supports_simple_order_by_label"
    setting.

    """

    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "some_table",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("x", Integer),
            Column("y", Integer),
            Column("q", String(50)),
            Column("p", String(50)),
        )

    @classmethod
    def insert_data(cls, connection):
        connection.execute(
            cls.tables.some_table.insert(),
            [
                {"id": 1, "x": 1, "y": 2, "q": "q1", "p": "p3"},
                {"id": 2, "x": 2, "y": 3, "q": "q2", "p": "p2"},
                {"id": 3, "x": 3, "y": 4, "q": "q3", "p": "p1"},
            ],
        )

    def _assert_result(self, select, result):
        with config.db.connect() as conn:
            eq_(conn.execute(select).fetchall(), result)

    def test_plain(self):
        table = self.tables.some_table
        lx = table.c.x.label("lx")
        self._assert_result(select(lx).order_by(lx), [(1,), (2,), (3,)])

    def test_composed_int(self):
        table = self.tables.some_table
        lx = (table.c.x + table.c.y).label("lx")
        self._assert_result(select(lx).order_by(lx), [(3,), (5,), (7,)])

    def test_composed_multiple(self):
        table = self.tables.some_table
        lx = (table.c.x + table.c.y).label("lx")
        ly = (func.lower(table.c.q) + table.c.p).label("ly")
        self._assert_result(
            select(lx, ly).order_by(lx, ly.desc()),
            [(3, "q1p3"), (5, "q2p2"), (7, "q3p1")],
        )

    def test_plain_desc(self):
        table = self.tables.some_table
        lx = table.c.x.label("lx")
        self._assert_result(select(lx).order_by(lx.desc()), [(3,), (2,), (1,)])

    def test_composed_int_desc(self):
        table = self.tables.some_table
        lx = (table.c.x + table.c.y).label("lx")
        self._assert_result(select(lx).order_by(lx.desc()), [(7,), (5,), (3,)])

    @testing.requires.group_by_complex_expression
    def test_group_by_composed(self):
        table = self.tables.some_table
        expr = (table.c.x + table.c.y).label("lx")
        stmt = (
            select(func.count(table.c.id), expr).group_by(expr).order_by(expr)
        )
        self._assert_result(stmt, [(1, 3), (1, 5), (1, 7)])


class ValuesExpressionTest(fixtures.TestBase):
    __requires__ = ("table_value_constructor",)

    __backend__ = True

    def test_tuples(self, connection):
        value_expr = values(
            column("id", Integer), column("name", String), name="my_values"
        ).data([(1, "name1"), (2, "name2"), (3, "name3")])

        eq_(
            connection.execute(select(value_expr)).all(),
            [(1, "name1"), (2, "name2"), (3, "name3")],
        )


class FetchLimitOffsetTest(fixtures.TablesTest):
    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "some_table",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("x", Integer),
            Column("y", Integer),
        )

    @classmethod
    def insert_data(cls, connection):
        connection.execute(
            cls.tables.some_table.insert(),
            [
                {"id": 1, "x": 1, "y": 2},
                {"id": 2, "x": 2, "y": 3},
                {"id": 3, "x": 3, "y": 4},
                {"id": 4, "x": 4, "y": 5},
                {"id": 5, "x": 4, "y": 6},
            ],
        )

    def _assert_result(
        self, connection, select, result, params=(), set_=False
    ):
        if set_:
            query_res = connection.execute(select, params).fetchall()
            eq_(len(query_res), len(result))
            eq_(set(query_res), set(result))

        else:
            eq_(connection.execute(select, params).fetchall(), result)

    def _assert_result_str(self, select, result, params=()):
        with config.db.connect() as conn:
            eq_(conn.exec_driver_sql(select, params).fetchall(), result)

    def test_simple_limit(self, connection):
        table = self.tables.some_table
        stmt = select(table).order_by(table.c.id)
        self._assert_result(
            connection,
            stmt.limit(2),
            [(1, 1, 2), (2, 2, 3)],
        )
        self._assert_result(
            connection,
            stmt.limit(3),
            [(1, 1, 2), (2, 2, 3), (3, 3, 4)],
        )

    def test_limit_render_multiple_times(self, connection):
        table = self.tables.some_table
        stmt = select(table.c.id).limit(1).scalar_subquery()

        u = union(select(stmt), select(stmt)).subquery().select()

        self._assert_result(
            connection,
            u,
            [
                (1,),
            ],
        )

    @testing.requires.fetch_first
    def test_simple_fetch(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table).order_by(table.c.id).fetch(2),
            [(1, 1, 2), (2, 2, 3)],
        )
        self._assert_result(
            connection,
            select(table).order_by(table.c.id).fetch(3),
            [(1, 1, 2), (2, 2, 3), (3, 3, 4)],
        )

    @testing.requires.offset
    def test_simple_offset(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table).order_by(table.c.id).offset(2),
            [(3, 3, 4), (4, 4, 5), (5, 4, 6)],
        )
        self._assert_result(
            connection,
            select(table).order_by(table.c.id).offset(3),
            [(4, 4, 5), (5, 4, 6)],
        )

    @testing.combinations(
        ([(2, 0), (2, 1), (3, 2)]),
        ([(2, 1), (2, 0), (3, 2)]),
        ([(3, 1), (2, 1), (3, 1)]),
        argnames="cases",
    )
    @testing.requires.offset
    def test_simple_limit_offset(self, connection, cases):
        table = self.tables.some_table
        connection = connection.execution_options(compiled_cache={})

        assert_data = [(1, 1, 2), (2, 2, 3), (3, 3, 4), (4, 4, 5), (5, 4, 6)]

        for limit, offset in cases:
            expected = assert_data[offset : offset + limit]
            self._assert_result(
                connection,
                select(table).order_by(table.c.id).limit(limit).offset(offset),
                expected,
            )

    @testing.requires.fetch_first
    def test_simple_fetch_offset(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table).order_by(table.c.id).fetch(2).offset(1),
            [(2, 2, 3), (3, 3, 4)],
        )

        self._assert_result(
            connection,
            select(table).order_by(table.c.id).fetch(3).offset(2),
            [(3, 3, 4), (4, 4, 5), (5, 4, 6)],
        )

    @testing.requires.fetch_no_order_by
    def test_fetch_offset_no_order(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table).fetch(10),
            [(1, 1, 2), (2, 2, 3), (3, 3, 4), (4, 4, 5), (5, 4, 6)],
            set_=True,
        )

    @testing.requires.offset
    def test_simple_offset_zero(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table).order_by(table.c.id).offset(0),
            [(1, 1, 2), (2, 2, 3), (3, 3, 4), (4, 4, 5), (5, 4, 6)],
        )

        self._assert_result(
            connection,
            select(table).order_by(table.c.id).offset(1),
            [(2, 2, 3), (3, 3, 4), (4, 4, 5), (5, 4, 6)],
        )

    @testing.requires.offset
    def test_limit_offset_nobinds(self):
        """test that 'literal binds' mode works - no bound params."""

        table = self.tables.some_table
        stmt = select(table).order_by(table.c.id).limit(2).offset(1)
        sql = stmt.compile(
            dialect=config.db.dialect, compile_kwargs={"literal_binds": True}
        )
        sql = str(sql)

        self._assert_result_str(sql, [(2, 2, 3), (3, 3, 4)])

    @testing.requires.fetch_first
    def test_fetch_offset_nobinds(self):
        """test that 'literal binds' mode works - no bound params."""

        table = self.tables.some_table
        stmt = select(table).order_by(table.c.id).fetch(2).offset(1)
        sql = stmt.compile(
            dialect=config.db.dialect, compile_kwargs={"literal_binds": True}
        )
        sql = str(sql)

        self._assert_result_str(sql, [(2, 2, 3), (3, 3, 4)])

    @testing.requires.bound_limit_offset
    def test_bound_limit(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table).order_by(table.c.id).limit(bindparam("l")),
            [(1, 1, 2), (2, 2, 3)],
            params={"l": 2},
        )

        self._assert_result(
            connection,
            select(table).order_by(table.c.id).limit(bindparam("l")),
            [(1, 1, 2), (2, 2, 3), (3, 3, 4)],
            params={"l": 3},
        )

    @testing.requires.bound_limit_offset
    def test_bound_offset(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table).order_by(table.c.id).offset(bindparam("o")),
            [(3, 3, 4), (4, 4, 5), (5, 4, 6)],
            params={"o": 2},
        )

        self._assert_result(
            connection,
            select(table).order_by(table.c.id).offset(bindparam("o")),
            [(2, 2, 3), (3, 3, 4), (4, 4, 5), (5, 4, 6)],
            params={"o": 1},
        )

    @testing.requires.bound_limit_offset
    def test_bound_limit_offset(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .limit(bindparam("l"))
            .offset(bindparam("o")),
            [(2, 2, 3), (3, 3, 4)],
            params={"l": 2, "o": 1},
        )

        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .limit(bindparam("l"))
            .offset(bindparam("o")),
            [(3, 3, 4), (4, 4, 5), (5, 4, 6)],
            params={"l": 3, "o": 2},
        )

    @testing.requires.fetch_first
    def test_bound_fetch_offset(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .fetch(bindparam("f"))
            .offset(bindparam("o")),
            [(2, 2, 3), (3, 3, 4)],
            params={"f": 2, "o": 1},
        )

        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .fetch(bindparam("f"))
            .offset(bindparam("o")),
            [(3, 3, 4), (4, 4, 5), (5, 4, 6)],
            params={"f": 3, "o": 2},
        )

    @testing.requires.sql_expression_limit_offset
    def test_expr_offset(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .offset(literal_column("1") + literal_column("2")),
            [(4, 4, 5), (5, 4, 6)],
        )

    @testing.requires.sql_expression_limit_offset
    def test_expr_limit(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .limit(literal_column("1") + literal_column("2")),
            [(1, 1, 2), (2, 2, 3), (3, 3, 4)],
        )

    @testing.requires.sql_expression_limit_offset
    def test_expr_limit_offset(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .limit(literal_column("1") + literal_column("1"))
            .offset(literal_column("1") + literal_column("1")),
            [(3, 3, 4), (4, 4, 5)],
        )

    @testing.requires.fetch_first
    @testing.requires.fetch_expression
    def test_expr_fetch_offset(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .fetch(literal_column("1") + literal_column("1"))
            .offset(literal_column("1") + literal_column("1")),
            [(3, 3, 4), (4, 4, 5)],
        )

    @testing.requires.sql_expression_limit_offset
    def test_simple_limit_expr_offset(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .limit(2)
            .offset(literal_column("1") + literal_column("1")),
            [(3, 3, 4), (4, 4, 5)],
        )

        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .limit(3)
            .offset(literal_column("1") + literal_column("1")),
            [(3, 3, 4), (4, 4, 5), (5, 4, 6)],
        )

    @testing.requires.sql_expression_limit_offset
    def test_expr_limit_simple_offset(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .limit(literal_column("1") + literal_column("1"))
            .offset(2),
            [(3, 3, 4), (4, 4, 5)],
        )

        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .limit(literal_column("1") + literal_column("1"))
            .offset(1),
            [(2, 2, 3), (3, 3, 4)],
        )

    @testing.requires.fetch_ties
    def test_simple_fetch_ties(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table).order_by(table.c.x.desc()).fetch(1, with_ties=True),
            [(4, 4, 5), (5, 4, 6)],
            set_=True,
        )

        self._assert_result(
            connection,
            select(table).order_by(table.c.x.desc()).fetch(3, with_ties=True),
            [(3, 3, 4), (4, 4, 5), (5, 4, 6)],
            set_=True,
        )

    @testing.requires.fetch_ties
    @testing.requires.fetch_offset_with_options
    def test_fetch_offset_ties(self, connection):
        table = self.tables.some_table
        fa = connection.execute(
            select(table)
            .order_by(table.c.x)
            .fetch(2, with_ties=True)
            .offset(2)
        ).fetchall()
        eq_(fa[0], (3, 3, 4))
        eq_(set(fa), set([(3, 3, 4), (4, 4, 5), (5, 4, 6)]))

    @testing.requires.fetch_ties
    @testing.requires.fetch_offset_with_options
    def test_fetch_offset_ties_exact_number(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.x)
            .fetch(2, with_ties=True)
            .offset(1),
            [(2, 2, 3), (3, 3, 4)],
        )

        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.x)
            .fetch(3, with_ties=True)
            .offset(3),
            [(4, 4, 5), (5, 4, 6)],
        )

    @testing.requires.fetch_percent
    def test_simple_fetch_percent(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table).order_by(table.c.id).fetch(20, percent=True),
            [(1, 1, 2)],
        )

    @testing.requires.fetch_percent
    @testing.requires.fetch_offset_with_options
    def test_fetch_offset_percent(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.id)
            .fetch(40, percent=True)
            .offset(1),
            [(2, 2, 3), (3, 3, 4)],
        )

    @testing.requires.fetch_ties
    @testing.requires.fetch_percent
    def test_simple_fetch_percent_ties(self, connection):
        table = self.tables.some_table
        self._assert_result(
            connection,
            select(table)
            .order_by(table.c.x.desc())
            .fetch(20, percent=True, with_ties=True),
            [(4, 4, 5), (5, 4, 6)],
            set_=True,
        )

    @testing.requires.fetch_ties
    @testing.requires.fetch_percent
    @testing.requires.fetch_offset_with_options
    def test_fetch_offset_percent_ties(self, connection):
        table = self.tables.some_table
        fa = connection.execute(
            select(table)
            .order_by(table.c.x)
            .fetch(40, percent=True, with_ties=True)
            .offset(2)
        ).fetchall()
        eq_(fa[0], (3, 3, 4))
        eq_(set(fa), set([(3, 3, 4), (4, 4, 5), (5, 4, 6)]))


class SameNamedSchemaTableTest(fixtures.TablesTest):
    """tests for #7471"""

    __backend__ = True

    __requires__ = ("schemas",)

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "some_table",
            metadata,
            Column("id", Integer, primary_key=True),
            schema=config.test_schema,
        )
        Table(
            "some_table",
            metadata,
            Column("id", Integer, primary_key=True),
            Column(
                "some_table_id",
                Integer,
                # ForeignKey("%s.some_table.id" % config.test_schema),
                nullable=False,
            ),
        )

    @classmethod
    def insert_data(cls, connection):
        some_table, some_table_schema = cls.tables(
            "some_table", "%s.some_table" % config.test_schema
        )
        connection.execute(some_table_schema.insert(), {"id": 1})
        connection.execute(some_table.insert(), {"id": 1, "some_table_id": 1})

    def test_simple_join_both_tables(self, connection):
        some_table, some_table_schema = self.tables(
            "some_table", "%s.some_table" % config.test_schema
        )

        eq_(
            connection.execute(
                select(some_table, some_table_schema).join_from(
                    some_table,
                    some_table_schema,
                    some_table.c.some_table_id == some_table_schema.c.id,
                )
            ).first(),
            (1, 1, 1),
        )

    def test_simple_join_whereclause_only(self, connection):
        some_table, some_table_schema = self.tables(
            "some_table", "%s.some_table" % config.test_schema
        )

        eq_(
            connection.execute(
                select(some_table)
                .join_from(
                    some_table,
                    some_table_schema,
                    some_table.c.some_table_id == some_table_schema.c.id,
                )
                .where(some_table.c.id == 1)
            ).first(),
            (1, 1),
        )

    def test_subquery(self, connection):
        some_table, some_table_schema = self.tables(
            "some_table", "%s.some_table" % config.test_schema
        )

        subq = (
            select(some_table)
            .join_from(
                some_table,
                some_table_schema,
                some_table.c.some_table_id == some_table_schema.c.id,
            )
            .where(some_table.c.id == 1)
            .subquery()
        )

        eq_(
            connection.execute(
                select(some_table, subq.c.id)
                .join_from(
                    some_table,
                    subq,
                    some_table.c.some_table_id == subq.c.id,
                )
                .where(some_table.c.id == 1)
            ).first(),
            (1, 1, 1),
        )


class JoinTest(fixtures.TablesTest):
    __backend__ = True

    def _assert_result(self, select, result, params=()):
        with config.db.connect() as conn:
            eq_(conn.execute(select, params).fetchall(), result)

    @classmethod
    def define_tables(cls, metadata):
        Table("a", metadata, Column("id", Integer, primary_key=True))
        Table(
            "b",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("a_id", ForeignKey("a.id"), nullable=False),
        )

    @classmethod
    def insert_data(cls, connection):
        connection.execute(
            cls.tables.a.insert(),
            [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}],
        )

        connection.execute(
            cls.tables.b.insert(),
            [
                {"id": 1, "a_id": 1},
                {"id": 2, "a_id": 1},
                {"id": 4, "a_id": 2},
                {"id": 5, "a_id": 3},
            ],
        )

    def test_inner_join_fk(self):
        a, b = self.tables("a", "b")

        stmt = select(a, b).select_from(a.join(b)).order_by(a.c.id, b.c.id)

        self._assert_result(stmt, [(1, 1, 1), (1, 2, 1), (2, 4, 2), (3, 5, 3)])

    def test_inner_join_true(self):
        a, b = self.tables("a", "b")

        stmt = (
            select(a, b)
            .select_from(a.join(b, true()))
            .order_by(a.c.id, b.c.id)
        )

        self._assert_result(
            stmt,
            [
                (a, b, c)
                for (a,), (b, c) in itertools.product(
                    [(1,), (2,), (3,), (4,), (5,)],
                    [(1, 1), (2, 1), (4, 2), (5, 3)],
                )
            ],
        )

    def test_inner_join_false(self):
        a, b = self.tables("a", "b")

        stmt = (
            select(a, b)
            .select_from(a.join(b, false()))
            .order_by(a.c.id, b.c.id)
        )

        self._assert_result(stmt, [])

    def test_outer_join_false(self):
        a, b = self.tables("a", "b")

        stmt = (
            select(a, b)
            .select_from(a.outerjoin(b, false()))
            .order_by(a.c.id, b.c.id)
        )

        self._assert_result(
            stmt,
            [
                (1, None, None),
                (2, None, None),
                (3, None, None),
                (4, None, None),
                (5, None, None),
            ],
        )

    def test_outer_join_fk(self):
        a, b = self.tables("a", "b")

        stmt = select(a, b).select_from(a.join(b)).order_by(a.c.id, b.c.id)

        self._assert_result(stmt, [(1, 1, 1), (1, 2, 1), (2, 4, 2), (3, 5, 3)])


class CompoundSelectTest(fixtures.TablesTest):
    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "some_table",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("x", Integer),
            Column("y", Integer),
        )

    @classmethod
    def insert_data(cls, connection):
        connection.execute(
            cls.tables.some_table.insert(),
            [
                {"id": 1, "x": 1, "y": 2},
                {"id": 2, "x": 2, "y": 3},
                {"id": 3, "x": 3, "y": 4},
                {"id": 4, "x": 4, "y": 5},
            ],
        )

    def _assert_result(self, select, result, params=()):
        with config.db.connect() as conn:
            eq_(conn.execute(select, params).fetchall(), result)

    def test_plain_union(self):
        table = self.tables.some_table
        s1 = select(table).where(table.c.id == 2)
        s2 = select(table).where(table.c.id == 3)

        u1 = union(s1, s2)
        self._assert_result(
            u1.order_by(u1.selected_columns.id), [(2, 2, 3), (3, 3, 4)]
        )

    def test_select_from_plain_union(self):
        table = self.tables.some_table
        s1 = select(table).where(table.c.id == 2)
        s2 = select(table).where(table.c.id == 3)

        u1 = union(s1, s2).alias().select()
        self._assert_result(
            u1.order_by(u1.selected_columns.id), [(2, 2, 3), (3, 3, 4)]
        )

    @testing.requires.order_by_col_from_union
    @testing.requires.parens_in_union_contained_select_w_limit_offset
    def test_limit_offset_selectable_in_unions(self):
        table = self.tables.some_table
        s1 = select(table).where(table.c.id == 2).limit(1).order_by(table.c.id)
        s2 = select(table).where(table.c.id == 3).limit(1).order_by(table.c.id)

        u1 = union(s1, s2).limit(2)
        self._assert_result(
            u1.order_by(u1.selected_columns.id), [(2, 2, 3), (3, 3, 4)]
        )

    @testing.requires.parens_in_union_contained_select_wo_limit_offset
    def test_order_by_selectable_in_unions(self):
        table = self.tables.some_table
        s1 = select(table).where(table.c.id == 2).order_by(table.c.id)
        s2 = select(table).where(table.c.id == 3).order_by(table.c.id)

        u1 = union(s1, s2).limit(2)
        self._assert_result(
            u1.order_by(u1.selected_columns.id), [(2, 2, 3), (3, 3, 4)]
        )

    def test_distinct_selectable_in_unions(self):
        table = self.tables.some_table
        s1 = select(table).where(table.c.id == 2).distinct()
        s2 = select(table).where(table.c.id == 3).distinct()

        u1 = union(s1, s2).limit(2)
        self._assert_result(
            u1.order_by(u1.selected_columns.id), [(2, 2, 3), (3, 3, 4)]
        )

    @testing.requires.parens_in_union_contained_select_w_limit_offset
    def test_limit_offset_in_unions_from_alias(self):
        table = self.tables.some_table
        s1 = select(table).where(table.c.id == 2).limit(1).order_by(table.c.id)
        s2 = select(table).where(table.c.id == 3).limit(1).order_by(table.c.id)

        # this necessarily has double parens
        u1 = union(s1, s2).alias()
        self._assert_result(
            u1.select().limit(2).order_by(u1.c.id), [(2, 2, 3), (3, 3, 4)]
        )

    def test_limit_offset_aliased_selectable_in_unions(self):
        table = self.tables.some_table
        s1 = (
            select(table)
            .where(table.c.id == 2)
            .limit(1)
            .order_by(table.c.id)
            .alias()
            .select()
        )
        s2 = (
            select(table)
            .where(table.c.id == 3)
            .limit(1)
            .order_by(table.c.id)
            .alias()
            .select()
        )

        u1 = union(s1, s2).limit(2)
        self._assert_result(
            u1.order_by(u1.selected_columns.id), [(2, 2, 3), (3, 3, 4)]
        )


class PostCompileParamsTest(
    AssertsExecutionResults, AssertsCompiledSQL, fixtures.TablesTest
):
    __backend__ = True

    __requires__ = ("standard_cursor_sql",)

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "some_table",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("x", Integer),
            Column("y", Integer),
            Column("z", String(50)),
        )

    @classmethod
    def insert_data(cls, connection):
        connection.execute(
            cls.tables.some_table.insert(),
            [
                {"id": 1, "x": 1, "y": 2, "z": "z1"},
                {"id": 2, "x": 2, "y": 3, "z": "z2"},
                {"id": 3, "x": 3, "y": 4, "z": "z3"},
                {"id": 4, "x": 4, "y": 5, "z": "z4"},
            ],
        )

    def test_compile(self):
        table = self.tables.some_table

        stmt = select(table.c.id).where(
            table.c.x == bindparam("q", literal_execute=True)
        )

        self.assert_compile(
            stmt,
            "SELECT some_table.id FROM some_table "
            "WHERE some_table.x = __[POSTCOMPILE_q]",
            {},
        )

    def test_compile_literal_binds(self):
        table = self.tables.some_table

        stmt = select(table.c.id).where(
            table.c.x == bindparam("q", 10, literal_execute=True)
        )

        self.assert_compile(
            stmt,
            "SELECT some_table.id FROM some_table WHERE some_table.x = 10",
            {},
            literal_binds=True,
        )

    def test_execute(self):
        table = self.tables.some_table

        stmt = select(table.c.id).where(
            table.c.x == bindparam("q", literal_execute=True)
        )

        with self.sql_execution_asserter() as asserter:
            with config.db.connect() as conn:
                conn.execute(stmt, dict(q=10))

        asserter.assert_(
            CursorSQL(
                "SELECT some_table.id \nFROM some_table "
                "\nWHERE some_table.x = 10",
                () if config.db.dialect.positional else {},
            )
        )

    def test_execute_expanding_plus_literal_execute(self):
        table = self.tables.some_table

        stmt = select(table.c.id).where(
            table.c.x.in_(bindparam("q", expanding=True, literal_execute=True))
        )

        with self.sql_execution_asserter() as asserter:
            with config.db.connect() as conn:
                conn.execute(stmt, dict(q=[5, 6, 7]))

        asserter.assert_(
            CursorSQL(
                "SELECT some_table.id \nFROM some_table "
                "\nWHERE some_table.x IN (5, 6, 7)",
                () if config.db.dialect.positional else {},
            )
        )

    @testing.requires.tuple_in
    def test_execute_tuple_expanding_plus_literal_execute(self):
        table = self.tables.some_table

        stmt = select(table.c.id).where(
            tuple_(table.c.x, table.c.y).in_(
                bindparam("q", expanding=True, literal_execute=True)
            )
        )

        with self.sql_execution_asserter() as asserter:
            with config.db.connect() as conn:
                conn.execute(stmt, dict(q=[(5, 10), (12, 18)]))

        asserter.assert_(
            CursorSQL(
                "SELECT some_table.id \nFROM some_table "
                "\nWHERE (some_table.x, some_table.y) "
                "IN (%s(5, 10), (12, 18))"
                % ("VALUES " if config.db.dialect.tuple_in_values else ""),
                () if config.db.dialect.positional else {},
            )
        )

    @testing.requires.tuple_in
    def test_execute_tuple_expanding_plus_literal_heterogeneous_execute(self):
        table = self.tables.some_table

        stmt = select(table.c.id).where(
            tuple_(table.c.x, table.c.z).in_(
                bindparam("q", expanding=True, literal_execute=True)
            )
        )

        with self.sql_execution_asserter() as asserter:
            with config.db.connect() as conn:
                conn.execute(stmt, dict(q=[(5, "z1"), (12, "z3")]))

        asserter.assert_(
            CursorSQL(
                "SELECT some_table.id \nFROM some_table "
                "\nWHERE (some_table.x, some_table.z) "
                "IN (%s(5, 'z1'), (12, 'z3'))"
                % ("VALUES " if config.db.dialect.tuple_in_values else ""),
                () if config.db.dialect.positional else {},
            )
        )


class ExpandingBoundInTest(fixtures.TablesTest):
    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "some_table",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("x", Integer),
            Column("y", Integer),
            Column("z", String(50)),
        )

    @classmethod
    def insert_data(cls, connection):
        connection.execute(
            cls.tables.some_table.insert(),
            [
                {"id": 1, "x": 1, "y": 2, "z": "z1"},
                {"id": 2, "x": 2, "y": 3, "z": "z2"},
                {"id": 3, "x": 3, "y": 4, "z": "z3"},
                {"id": 4, "x": 4, "y": 5, "z": "z4"},
            ],
        )

    def _assert_result(self, select, result, params=()):
        with config.db.connect() as conn:
            eq_(conn.execute(select, params).fetchall(), result)

    def test_multiple_empty_sets_bindparam(self):
        # test that any anonymous aliasing used by the dialect
        # is fine with duplicates
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(table.c.x.in_(bindparam("q")))
            .where(table.c.y.in_(bindparam("p")))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [], params={"q": [], "p": []})

    def test_multiple_empty_sets_direct(self):
        # test that any anonymous aliasing used by the dialect
        # is fine with duplicates
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(table.c.x.in_([]))
            .where(table.c.y.in_([]))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [])

    @testing.requires.tuple_in_w_empty
    def test_empty_heterogeneous_tuples_bindparam(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(tuple_(table.c.x, table.c.z).in_(bindparam("q")))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [], params={"q": []})

    @testing.requires.tuple_in_w_empty
    def test_empty_heterogeneous_tuples_direct(self):
        table = self.tables.some_table

        def go(val, expected):
            stmt = (
                select(table.c.id)
                .where(tuple_(table.c.x, table.c.z).in_(val))
                .order_by(table.c.id)
            )
            self._assert_result(stmt, expected)

        go([], [])
        go([(2, "z2"), (3, "z3"), (4, "z4")], [(2,), (3,), (4,)])
        go([], [])

    @testing.requires.tuple_in_w_empty
    def test_empty_homogeneous_tuples_bindparam(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(tuple_(table.c.x, table.c.y).in_(bindparam("q")))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [], params={"q": []})

    @testing.requires.tuple_in_w_empty
    def test_empty_homogeneous_tuples_direct(self):
        table = self.tables.some_table

        def go(val, expected):
            stmt = (
                select(table.c.id)
                .where(tuple_(table.c.x, table.c.y).in_(val))
                .order_by(table.c.id)
            )
            self._assert_result(stmt, expected)

        go([], [])
        go([(1, 2), (2, 3), (3, 4)], [(1,), (2,), (3,)])
        go([], [])

    def test_bound_in_scalar_bindparam(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(table.c.x.in_(bindparam("q")))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [(2,), (3,), (4,)], params={"q": [2, 3, 4]})

    def test_bound_in_scalar_direct(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(table.c.x.in_([2, 3, 4]))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [(2,), (3,), (4,)])

    def test_nonempty_in_plus_empty_notin(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(table.c.x.in_([2, 3]))
            .where(table.c.id.not_in([]))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [(2,), (3,)])

    def test_empty_in_plus_notempty_notin(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(table.c.x.in_([]))
            .where(table.c.id.not_in([2, 3]))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [])

    def test_typed_str_in(self):
        """test related to #7292.

        as a type is given to the bound param, there is no ambiguity
        to the type of element.

        """

        stmt = text(
            "select id FROM some_table WHERE z IN :q ORDER BY id"
        ).bindparams(bindparam("q", type_=String, expanding=True))
        self._assert_result(
            stmt,
            [(2,), (3,), (4,)],
            params={"q": ["z2", "z3", "z4"]},
        )

    def test_untyped_str_in(self):
        """test related to #7292.

        for untyped expression, we look at the types of elements.
        Test for Sequence to detect tuple in.  but not strings or bytes!
        as always....

        """

        stmt = text(
            "select id FROM some_table WHERE z IN :q ORDER BY id"
        ).bindparams(bindparam("q", expanding=True))
        self._assert_result(
            stmt,
            [(2,), (3,), (4,)],
            params={"q": ["z2", "z3", "z4"]},
        )

    @testing.requires.tuple_in
    def test_bound_in_two_tuple_bindparam(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(tuple_(table.c.x, table.c.y).in_(bindparam("q")))
            .order_by(table.c.id)
        )
        self._assert_result(
            stmt, [(2,), (3,), (4,)], params={"q": [(2, 3), (3, 4), (4, 5)]}
        )

    @testing.requires.tuple_in
    def test_bound_in_two_tuple_direct(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(tuple_(table.c.x, table.c.y).in_([(2, 3), (3, 4), (4, 5)]))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [(2,), (3,), (4,)])

    @testing.requires.tuple_in
    def test_bound_in_heterogeneous_two_tuple_bindparam(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(tuple_(table.c.x, table.c.z).in_(bindparam("q")))
            .order_by(table.c.id)
        )
        self._assert_result(
            stmt,
            [(2,), (3,), (4,)],
            params={"q": [(2, "z2"), (3, "z3"), (4, "z4")]},
        )

    @testing.requires.tuple_in
    def test_bound_in_heterogeneous_two_tuple_direct(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(
                tuple_(table.c.x, table.c.z).in_(
                    [(2, "z2"), (3, "z3"), (4, "z4")]
                )
            )
            .order_by(table.c.id)
        )
        self._assert_result(
            stmt,
            [(2,), (3,), (4,)],
        )

    @testing.requires.tuple_in
    def test_bound_in_heterogeneous_two_tuple_text_bindparam(self):
        # note this becomes ARRAY if we dont use expanding
        # explicitly right now
        stmt = text(
            "select id FROM some_table WHERE (x, z) IN :q ORDER BY id"
        ).bindparams(bindparam("q", expanding=True))
        self._assert_result(
            stmt,
            [(2,), (3,), (4,)],
            params={"q": [(2, "z2"), (3, "z3"), (4, "z4")]},
        )

    @testing.requires.tuple_in
    def test_bound_in_heterogeneous_two_tuple_typed_bindparam_non_tuple(self):
        class LikeATuple(collections_abc.Sequence):
            def __init__(self, *data):
                self._data = data

            def __iter__(self):
                return iter(self._data)

            def __getitem__(self, idx):
                return self._data[idx]

            def __len__(self):
                return len(self._data)

        stmt = text(
            "select id FROM some_table WHERE (x, z) IN :q ORDER BY id"
        ).bindparams(
            bindparam(
                "q", type_=TupleType(Integer(), String()), expanding=True
            )
        )
        self._assert_result(
            stmt,
            [(2,), (3,), (4,)],
            params={
                "q": [
                    LikeATuple(2, "z2"),
                    LikeATuple(3, "z3"),
                    LikeATuple(4, "z4"),
                ]
            },
        )

    @testing.requires.tuple_in
    def test_bound_in_heterogeneous_two_tuple_text_bindparam_non_tuple(self):
        # note this becomes ARRAY if we dont use expanding
        # explicitly right now

        class LikeATuple(collections_abc.Sequence):
            def __init__(self, *data):
                self._data = data

            def __iter__(self):
                return iter(self._data)

            def __getitem__(self, idx):
                return self._data[idx]

            def __len__(self):
                return len(self._data)

        stmt = text(
            "select id FROM some_table WHERE (x, z) IN :q ORDER BY id"
        ).bindparams(bindparam("q", expanding=True))
        self._assert_result(
            stmt,
            [(2,), (3,), (4,)],
            params={
                "q": [
                    LikeATuple(2, "z2"),
                    LikeATuple(3, "z3"),
                    LikeATuple(4, "z4"),
                ]
            },
        )

    def test_empty_set_against_integer_bindparam(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(table.c.x.in_(bindparam("q")))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [], params={"q": []})

    def test_empty_set_against_integer_direct(self):
        table = self.tables.some_table
        stmt = select(table.c.id).where(table.c.x.in_([])).order_by(table.c.id)
        self._assert_result(stmt, [])

    def test_empty_set_against_integer_negation_bindparam(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(table.c.x.not_in(bindparam("q")))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [(1,), (2,), (3,), (4,)], params={"q": []})

    def test_empty_set_against_integer_negation_direct(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id).where(table.c.x.not_in([])).order_by(table.c.id)
        )
        self._assert_result(stmt, [(1,), (2,), (3,), (4,)])

    def test_empty_set_against_string_bindparam(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(table.c.z.in_(bindparam("q")))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [], params={"q": []})

    def test_empty_set_against_string_direct(self):
        table = self.tables.some_table
        stmt = select(table.c.id).where(table.c.z.in_([])).order_by(table.c.id)
        self._assert_result(stmt, [])

    def test_empty_set_against_string_negation_bindparam(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id)
            .where(table.c.z.not_in(bindparam("q")))
            .order_by(table.c.id)
        )
        self._assert_result(stmt, [(1,), (2,), (3,), (4,)], params={"q": []})

    def test_empty_set_against_string_negation_direct(self):
        table = self.tables.some_table
        stmt = (
            select(table.c.id).where(table.c.z.not_in([])).order_by(table.c.id)
        )
        self._assert_result(stmt, [(1,), (2,), (3,), (4,)])

    def test_null_in_empty_set_is_false_bindparam(self, connection):
        stmt = select(
            case(
                (
                    null().in_(bindparam("foo", value=())),
                    true(),
                ),
                else_=false(),
            )
        )
        in_(connection.execute(stmt).fetchone()[0], (False, 0))

    def test_null_in_empty_set_is_false_direct(self, connection):
        stmt = select(
            case(
                (
                    null().in_([]),
                    true(),
                ),
                else_=false(),
            )
        )
        in_(connection.execute(stmt).fetchone()[0], (False, 0))


class LikeFunctionsTest(fixtures.TablesTest):
    __backend__ = True

    run_inserts = "once"
    run_deletes = None

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "some_table",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("data", String(50)),
        )

    @classmethod
    def insert_data(cls, connection):
        connection.execute(
            cls.tables.some_table.insert(),
            [
                {"id": 1, "data": "abcdefg"},
                {"id": 2, "data": "ab/cdefg"},
                {"id": 3, "data": "ab%cdefg"},
                {"id": 4, "data": "ab_cdefg"},
                {"id": 5, "data": "abcde/fg"},
                {"id": 6, "data": "abcde%fg"},
                {"id": 7, "data": "ab#cdefg"},
                {"id": 8, "data": "ab9cdefg"},
                {"id": 9, "data": "abcde#fg"},
                {"id": 10, "data": "abcd9fg"},
                {"id": 11, "data": None},
            ],
        )

    def _test(self, expr, expected):
        some_table = self.tables.some_table

        with config.db.connect() as conn:
            rows = {
                value
                for value, in conn.execute(select(some_table.c.id).where(expr))
            }

        eq_(rows, expected)

    def test_startswith_unescaped(self):
        col = self.tables.some_table.c.data
        self._test(col.startswith("ab%c"), {1, 2, 3, 4, 5, 6, 7, 8, 9, 10})

    def test_startswith_autoescape(self):
        col = self.tables.some_table.c.data
        self._test(col.startswith("ab%c", autoescape=True), {3})

    def test_startswith_sqlexpr(self):
        col = self.tables.some_table.c.data
        self._test(
            col.startswith(literal_column("'ab%c'")),
            {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
        )

    def test_startswith_escape(self):
        col = self.tables.some_table.c.data
        self._test(col.startswith("ab##c", escape="#"), {7})

    def test_startswith_autoescape_escape(self):
        col = self.tables.some_table.c.data
        self._test(col.startswith("ab%c", autoescape=True, escape="#"), {3})
        self._test(col.startswith("ab#c", autoescape=True, escape="#"), {7})

    def test_endswith_unescaped(self):
        col = self.tables.some_table.c.data
        self._test(col.endswith("e%fg"), {1, 2, 3, 4, 5, 6, 7, 8, 9})

    def test_endswith_sqlexpr(self):
        col = self.tables.some_table.c.data
        self._test(
            col.endswith(literal_column("'e%fg'")), {1, 2, 3, 4, 5, 6, 7, 8, 9}
        )

    def test_endswith_autoescape(self):
        col = self.tables.some_table.c.data
        self._test(col.endswith("e%fg", autoescape=True), {6})

    def test_endswith_escape(self):
        col = self.tables.some_table.c.data
        self._test(col.endswith("e##fg", escape="#"), {9})

    def test_endswith_autoescape_escape(self):
        col = self.tables.some_table.c.data
        self._test(col.endswith("e%fg", autoescape=True, escape="#"), {6})
        self._test(col.endswith("e#fg", autoescape=True, escape="#"), {9})

    def test_contains_unescaped(self):
        col = self.tables.some_table.c.data
        self._test(col.contains("b%cde"), {1, 2, 3, 4, 5, 6, 7, 8, 9})

    def test_contains_autoescape(self):
        col = self.tables.some_table.c.data
        self._test(col.contains("b%cde", autoescape=True), {3})

    def test_contains_escape(self):
        col = self.tables.some_table.c.data
        self._test(col.contains("b##cde", escape="#"), {7})

    def test_contains_autoescape_escape(self):
        col = self.tables.some_table.c.data
        self._test(col.contains("b%cd", autoescape=True, escape="#"), {3})
        self._test(col.contains("b#cd", autoescape=True, escape="#"), {7})

    @testing.requires.regexp_match
    def test_not_regexp_match(self):
        col = self.tables.some_table.c.data
        self._test(~col.regexp_match("a.cde"), {2, 3, 4, 7, 8, 10})

    @testing.requires.regexp_replace
    def test_regexp_replace(self):
        col = self.tables.some_table.c.data
        self._test(
            col.regexp_replace("a.cde", "FOO").contains("FOO"), {1, 5, 6, 9}
        )

    @testing.requires.regexp_match
    @testing.combinations(
        ("a.cde", {1, 5, 6, 9}),
        ("abc", {1, 5, 6, 9, 10}),
        ("^abc", {1, 5, 6, 9, 10}),
        ("9cde", {8}),
        ("^a", set(range(1, 11))),
        ("(b|c)", set(range(1, 11))),
        ("^(b|c)", set()),
    )
    def test_regexp_match(self, text, expected):
        col = self.tables.some_table.c.data
        self._test(col.regexp_match(text), expected)


class ComputedColumnTest(fixtures.TablesTest):
    __backend__ = True
    __requires__ = ("computed_columns",)

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "square",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("side", Integer),
            Column("area", Integer, Computed("side * side")),
            Column("perimeter", Integer, Computed("4 * side")),
        )

    @classmethod
    def insert_data(cls, connection):
        connection.execute(
            cls.tables.square.insert(),
            [{"id": 1, "side": 10}, {"id": 10, "side": 42}],
        )

    def test_select_all(self):
        with config.db.connect() as conn:
            res = conn.execute(
                select(text("*"))
                .select_from(self.tables.square)
                .order_by(self.tables.square.c.id)
            ).fetchall()
            eq_(res, [(1, 10, 100, 40), (10, 42, 1764, 168)])

    def test_select_columns(self):
        with config.db.connect() as conn:
            res = conn.execute(
                select(
                    self.tables.square.c.area, self.tables.square.c.perimeter
                )
                .select_from(self.tables.square)
                .order_by(self.tables.square.c.id)
            ).fetchall()
            eq_(res, [(100, 40), (1764, 168)])


class IdentityColumnTest(fixtures.TablesTest):
    __backend__ = True
    __requires__ = ("identity_columns",)
    run_inserts = "once"
    run_deletes = "once"

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "tbl_a",
            metadata,
            Column(
                "id",
                Integer,
                Identity(
                    always=True, start=42, nominvalue=True, nomaxvalue=True
                ),
                primary_key=True,
            ),
            Column("desc", String(100)),
        )
        Table(
            "tbl_b",
            metadata,
            Column(
                "id",
                Integer,
                Identity(increment=-5, start=0, minvalue=-1000, maxvalue=0),
                primary_key=True,
            ),
            Column("desc", String(100)),
        )

    @classmethod
    def insert_data(cls, connection):
        connection.execute(
            cls.tables.tbl_a.insert(),
            [{"desc": "a"}, {"desc": "b"}],
        )
        connection.execute(
            cls.tables.tbl_b.insert(),
            [{"desc": "a"}, {"desc": "b"}],
        )
        connection.execute(
            cls.tables.tbl_b.insert(),
            [{"id": 42, "desc": "c"}],
        )

    def test_select_all(self, connection):
        res = connection.execute(
            select(text("*"))
            .select_from(self.tables.tbl_a)
            .order_by(self.tables.tbl_a.c.id)
        ).fetchall()
        eq_(res, [(42, "a"), (43, "b")])

        res = connection.execute(
            select(text("*"))
            .select_from(self.tables.tbl_b)
            .order_by(self.tables.tbl_b.c.id)
        ).fetchall()
        eq_(res, [(-5, "b"), (0, "a"), (42, "c")])

    def test_select_columns(self, connection):

        res = connection.execute(
            select(self.tables.tbl_a.c.id).order_by(self.tables.tbl_a.c.id)
        ).fetchall()
        eq_(res, [(42,), (43,)])

    @testing.requires.identity_columns_standard
    def test_insert_always_error(self, connection):
        def fn():
            connection.execute(
                self.tables.tbl_a.insert(),
                [{"id": 200, "desc": "a"}],
            )

        assert_raises((DatabaseError, ProgrammingError), fn)


class IdentityAutoincrementTest(fixtures.TablesTest):
    __backend__ = True
    __requires__ = ("autoincrement_without_sequence",)

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "tbl",
            metadata,
            Column(
                "id",
                Integer,
                Identity(),
                primary_key=True,
                autoincrement=True,
            ),
            Column("desc", String(100)),
        )

    def test_autoincrement_with_identity(self, connection):
        res = connection.execute(self.tables.tbl.insert(), {"desc": "row"})
        res = connection.execute(self.tables.tbl.select()).first()
        eq_(res, (1, "row"))


class ExistsTest(fixtures.TablesTest):
    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "stuff",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("data", String(50)),
        )

    @classmethod
    def insert_data(cls, connection):
        connection.execute(
            cls.tables.stuff.insert(),
            [
                {"id": 1, "data": "some data"},
                {"id": 2, "data": "some data"},
                {"id": 3, "data": "some data"},
                {"id": 4, "data": "some other data"},
            ],
        )

    def test_select_exists(self, connection):
        stuff = self.tables.stuff
        eq_(
            connection.execute(
                select(literal(1)).where(
                    exists().where(stuff.c.data == "some data")
                )
            ).fetchall(),
            [(1,)],
        )

    def test_select_exists_false(self, connection):
        stuff = self.tables.stuff
        eq_(
            connection.execute(
                select(literal(1)).where(
                    exists().where(stuff.c.data == "no data")
                )
            ).fetchall(),
            [],
        )


class DistinctOnTest(AssertsCompiledSQL, fixtures.TablesTest):
    __backend__ = True

    @testing.fails_if(testing.requires.supports_distinct_on)
    def test_distinct_on(self):
        stm = select("*").distinct(column("q")).select_from(table("foo"))
        with testing.expect_deprecated(
            "DISTINCT ON is currently supported only by the PostgreSQL "
        ):
            self.assert_compile(stm, "SELECT DISTINCT * FROM foo")


class IsOrIsNotDistinctFromTest(fixtures.TablesTest):
    __backend__ = True
    __requires__ = ("supports_is_distinct_from",)

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "is_distinct_test",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("col_a", Integer, nullable=True),
            Column("col_b", Integer, nullable=True),
        )

    @testing.combinations(
        ("both_int_different", 0, 1, 1),
        ("both_int_same", 1, 1, 0),
        ("one_null_first", None, 1, 1),
        ("one_null_second", 0, None, 1),
        ("both_null", None, None, 0),
        id_="iaaa",
        argnames="col_a_value, col_b_value, expected_row_count_for_is",
    )
    def test_is_or_is_not_distinct_from(
        self, col_a_value, col_b_value, expected_row_count_for_is, connection
    ):
        tbl = self.tables.is_distinct_test

        connection.execute(
            tbl.insert(),
            [{"id": 1, "col_a": col_a_value, "col_b": col_b_value}],
        )

        result = connection.execute(
            tbl.select().where(tbl.c.col_a.is_distinct_from(tbl.c.col_b))
        ).fetchall()
        eq_(
            len(result),
            expected_row_count_for_is,
        )

        expected_row_count_for_is_not = (
            1 if expected_row_count_for_is == 0 else 0
        )
        result = connection.execute(
            tbl.select().where(tbl.c.col_a.is_not_distinct_from(tbl.c.col_b))
        ).fetchall()
        eq_(
            len(result),
            expected_row_count_for_is_not,
        )
