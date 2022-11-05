#! coding: utf-8

from . import testing
from .. import assert_raises
from .. import config
from .. import engines
from .. import eq_
from .. import fixtures
from .. import ne_
from .. import provide_metadata
from ..config import requirements
from ..provision import set_default_schema_on_connection
from ..schema import Column
from ..schema import Table
from ... import bindparam
from ... import event
from ... import exc
from ... import Integer
from ... import literal_column
from ... import select
from ... import String
from ...util import compat


class ExceptionTest(fixtures.TablesTest):
    """Test basic exception wrapping.

    DBAPIs vary a lot in exception behavior so to actually anticipate
    specific exceptions from real round trips, we need to be conservative.

    """

    run_deletes = "each"

    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "manual_pk",
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=False),
            Column("data", String(50)),
        )

    @requirements.duplicate_key_raises_integrity_error
    def test_integrity_error(self):

        with config.db.connect() as conn:

            trans = conn.begin()
            conn.execute(
                self.tables.manual_pk.insert(), {"id": 1, "data": "d1"}
            )

            assert_raises(
                exc.IntegrityError,
                conn.execute,
                self.tables.manual_pk.insert(),
                {"id": 1, "data": "d1"},
            )

            trans.rollback()

    def test_exception_with_non_ascii(self):
        with config.db.connect() as conn:
            try:
                # try to create an error message that likely has non-ascii
                # characters in the DBAPI's message string.  unfortunately
                # there's no way to make this happen with some drivers like
                # mysqlclient, pymysql.  this at least does produce a non-
                # ascii error message for cx_oracle, psycopg2
                conn.execute(select(literal_column(u"méil")))
                assert False
            except exc.DBAPIError as err:
                err_str = str(err)

                assert str(err.orig) in str(err)

            # test that we are actually getting string on Py2k, unicode
            # on Py3k.
            if compat.py2k:
                assert isinstance(err_str, str)
            else:
                assert isinstance(err_str, str)


class IsolationLevelTest(fixtures.TestBase):
    __backend__ = True

    __requires__ = ("isolation_level",)

    def _get_non_default_isolation_level(self):
        levels = requirements.get_isolation_levels(config)

        default = levels["default"]
        supported = levels["supported"]

        s = set(supported).difference(["AUTOCOMMIT", default])
        if s:
            return s.pop()
        else:
            config.skip_test("no non-default isolation level available")

    def test_default_isolation_level(self):
        eq_(
            config.db.dialect.default_isolation_level,
            requirements.get_isolation_levels(config)["default"],
        )

    def test_non_default_isolation_level(self):
        non_default = self._get_non_default_isolation_level()

        with config.db.connect() as conn:
            existing = conn.get_isolation_level()

            ne_(existing, non_default)

            conn.execution_options(isolation_level=non_default)

            eq_(conn.get_isolation_level(), non_default)

            conn.dialect.reset_isolation_level(conn.connection)

            eq_(conn.get_isolation_level(), existing)

    def test_all_levels(self):
        levels = requirements.get_isolation_levels(config)

        all_levels = levels["supported"]

        for level in set(all_levels).difference(["AUTOCOMMIT"]):
            with config.db.connect() as conn:
                conn.execution_options(isolation_level=level)

                eq_(conn.get_isolation_level(), level)

                trans = conn.begin()
                trans.rollback()

                eq_(conn.get_isolation_level(), level)

            with config.db.connect() as conn:
                eq_(
                    conn.get_isolation_level(),
                    levels["default"],
                )


class AutocommitIsolationTest(fixtures.TablesTest):

    run_deletes = "each"

    __requires__ = ("autocommit",)

    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "some_table",
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=False),
            Column("data", String(50)),
            test_needs_acid=True,
        )

    def _test_conn_autocommits(self, conn, autocommit):
        trans = conn.begin()
        conn.execute(
            self.tables.some_table.insert(), {"id": 1, "data": "some data"}
        )
        trans.rollback()

        eq_(
            conn.scalar(select(self.tables.some_table.c.id)),
            1 if autocommit else None,
        )

        with conn.begin():
            conn.execute(self.tables.some_table.delete())

    def test_autocommit_on(self, connection_no_trans):
        conn = connection_no_trans
        c2 = conn.execution_options(isolation_level="AUTOCOMMIT")
        self._test_conn_autocommits(c2, True)

        c2.dialect.reset_isolation_level(c2.connection)

        self._test_conn_autocommits(conn, False)

    def test_autocommit_off(self, connection_no_trans):
        conn = connection_no_trans
        self._test_conn_autocommits(conn, False)

    def test_turn_autocommit_off_via_default_iso_level(
        self, connection_no_trans
    ):
        conn = connection_no_trans
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        self._test_conn_autocommits(conn, True)

        conn.execution_options(
            isolation_level=requirements.get_isolation_levels(config)[
                "default"
            ]
        )
        self._test_conn_autocommits(conn, False)


class EscapingTest(fixtures.TestBase):
    @provide_metadata
    def test_percent_sign_round_trip(self):
        """test that the DBAPI accommodates for escaped / nonescaped
        percent signs in a way that matches the compiler

        """
        m = self.metadata
        t = Table("t", m, Column("data", String(50)))
        t.create(config.db)
        with config.db.begin() as conn:
            conn.execute(t.insert(), dict(data="some % value"))
            conn.execute(t.insert(), dict(data="some %% other value"))

            eq_(
                conn.scalar(
                    select(t.c.data).where(
                        t.c.data == literal_column("'some % value'")
                    )
                ),
                "some % value",
            )

            eq_(
                conn.scalar(
                    select(t.c.data).where(
                        t.c.data == literal_column("'some %% other value'")
                    )
                ),
                "some %% other value",
            )


class WeCanSetDefaultSchemaWEventsTest(fixtures.TestBase):
    __backend__ = True

    __requires__ = ("default_schema_name_switch",)

    def test_control_case(self):
        default_schema_name = config.db.dialect.default_schema_name

        eng = engines.testing_engine()
        with eng.connect():
            pass

        eq_(eng.dialect.default_schema_name, default_schema_name)

    def test_wont_work_wo_insert(self):
        default_schema_name = config.db.dialect.default_schema_name

        eng = engines.testing_engine()

        @event.listens_for(eng, "connect")
        def on_connect(dbapi_connection, connection_record):
            set_default_schema_on_connection(
                config, dbapi_connection, config.test_schema
            )

        with eng.connect() as conn:
            what_it_should_be = eng.dialect._get_default_schema_name(conn)
            eq_(what_it_should_be, config.test_schema)

        eq_(eng.dialect.default_schema_name, default_schema_name)

    def test_schema_change_on_connect(self):
        eng = engines.testing_engine()

        @event.listens_for(eng, "connect", insert=True)
        def on_connect(dbapi_connection, connection_record):
            set_default_schema_on_connection(
                config, dbapi_connection, config.test_schema
            )

        with eng.connect() as conn:
            what_it_should_be = eng.dialect._get_default_schema_name(conn)
            eq_(what_it_should_be, config.test_schema)

        eq_(eng.dialect.default_schema_name, config.test_schema)

    def test_schema_change_works_w_transactions(self):
        eng = engines.testing_engine()

        @event.listens_for(eng, "connect", insert=True)
        def on_connect(dbapi_connection, *arg):
            set_default_schema_on_connection(
                config, dbapi_connection, config.test_schema
            )

        with eng.connect() as conn:
            trans = conn.begin()
            what_it_should_be = eng.dialect._get_default_schema_name(conn)
            eq_(what_it_should_be, config.test_schema)
            trans.rollback()

            what_it_should_be = eng.dialect._get_default_schema_name(conn)
            eq_(what_it_should_be, config.test_schema)

        eq_(eng.dialect.default_schema_name, config.test_schema)


class FutureWeCanSetDefaultSchemaWEventsTest(
    fixtures.FutureEngineMixin, WeCanSetDefaultSchemaWEventsTest
):
    pass


class DifficultParametersTest(fixtures.TestBase):
    __backend__ = True

    @testing.combinations(
        ("boring",),
        ("per cent",),
        ("per % cent",),
        ("%percent",),
        ("par(ens)",),
        ("percent%(ens)yah",),
        ("col:ons",),
        ("_starts_with_underscore",),
        ("dot.s",),
        ("more :: %colons%",),
        ("/slashes/",),
        ("more/slashes",),
        ("q?marks",),
        ("1param",),
        ("1col:on",),
        argnames="name",
    )
    def test_round_trip(self, name, connection, metadata):
        t = Table(
            "t",
            metadata,
            Column("id", Integer, primary_key=True),
            Column(name, String(50), nullable=False),
        )

        # table is created
        t.create(connection)

        # automatic param generated by insert
        connection.execute(t.insert().values({"id": 1, name: "some name"}))

        # automatic param generated by criteria, plus selecting the column
        stmt = select(t.c[name]).where(t.c[name] == "some name")

        eq_(connection.scalar(stmt), "some name")

        # use the name in a param explicitly
        stmt = select(t.c[name]).where(t.c[name] == bindparam(name))

        row = connection.execute(stmt, {name: "some name"}).first()

        # name works as the key from cursor.description
        eq_(row._mapping[name], "some name")

        # use expanding IN
        stmt = select(t.c[name]).where(
            t.c[name].in_(["some name", "some other_name"])
        )

        row = connection.execute(stmt).first()
