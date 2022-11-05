# sql/dml.py
# Copyright (C) 2009-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php
"""
Provide :class:`_expression.Insert`, :class:`_expression.Update` and
:class:`_expression.Delete`.

"""
from sqlalchemy.types import NullType
from . import coercions
from . import roles
from . import util as sql_util
from .base import _entity_namespace_key
from .base import _exclusive_against
from .base import _from_objects
from .base import _generative
from .base import ColumnCollection
from .base import CompileState
from .base import DialectKWArgs
from .base import Executable
from .base import HasCompileState
from .elements import BooleanClauseList
from .elements import ClauseElement
from .elements import Null
from .selectable import HasCTE
from .selectable import HasPrefixes
from .selectable import ReturnsRows
from .visitors import InternalTraversal
from .. import exc
from .. import util
from ..util import collections_abc


class DMLState(CompileState):
    _no_parameters = True
    _dict_parameters = None
    _multi_parameters = None
    _ordered_values = None
    _parameter_ordering = None
    _has_multi_parameters = False
    isupdate = False
    isdelete = False
    isinsert = False

    def __init__(self, statement, compiler, **kw):
        raise NotImplementedError()

    @classmethod
    def get_entity_description(cls, statement):
        return {"name": statement.table.name, "table": statement.table}

    @classmethod
    def get_returning_column_descriptions(cls, statement):
        return [
            {
                "name": c.key,
                "type": c.type,
                "expr": c,
            }
            for c in statement._all_selected_columns
        ]

    @property
    def dml_table(self):
        return self.statement.table

    @classmethod
    def _get_crud_kv_pairs(cls, statement, kv_iterator):
        return [
            (
                coercions.expect(roles.DMLColumnRole, k),
                coercions.expect(
                    roles.ExpressionElementRole,
                    v,
                    type_=NullType(),
                    is_crud=True,
                ),
            )
            for k, v in kv_iterator
        ]

    def _make_extra_froms(self, statement):
        froms = []

        all_tables = list(sql_util.tables_from_leftmost(statement.table))
        seen = {all_tables[0]}

        for crit in statement._where_criteria:
            for item in _from_objects(crit):
                if not seen.intersection(item._cloned_set):
                    froms.append(item)
                seen.update(item._cloned_set)

        froms.extend(all_tables[1:])
        return froms

    def _process_multi_values(self, statement):
        if not statement._supports_multi_parameters:
            raise exc.InvalidRequestError(
                "%s construct does not support "
                "multiple parameter sets." % statement.__visit_name__.upper()
            )

        for parameters in statement._multi_values:
            multi_parameters = [
                {
                    c.key: value
                    for c, value in zip(statement.table.c, parameter_set)
                }
                if isinstance(parameter_set, collections_abc.Sequence)
                else parameter_set
                for parameter_set in parameters
            ]

            if self._no_parameters:
                self._no_parameters = False
                self._has_multi_parameters = True
                self._multi_parameters = multi_parameters
                self._dict_parameters = self._multi_parameters[0]
            elif not self._has_multi_parameters:
                self._cant_mix_formats_error()
            else:
                self._multi_parameters.extend(multi_parameters)

    def _process_values(self, statement):
        if self._no_parameters:
            self._has_multi_parameters = False
            self._dict_parameters = statement._values
            self._no_parameters = False
        elif self._has_multi_parameters:
            self._cant_mix_formats_error()

    def _process_ordered_values(self, statement):
        parameters = statement._ordered_values

        if self._no_parameters:
            self._no_parameters = False
            self._dict_parameters = dict(parameters)
            self._ordered_values = parameters
            self._parameter_ordering = [key for key, value in parameters]
        elif self._has_multi_parameters:
            self._cant_mix_formats_error()
        else:
            raise exc.InvalidRequestError(
                "Can only invoke ordered_values() once, and not mixed "
                "with any other values() call"
            )

    def _process_select_values(self, statement):
        parameters = {
            coercions.expect(roles.DMLColumnRole, name, as_key=True): Null()
            for name in statement._select_names
        }

        if self._no_parameters:
            self._no_parameters = False
            self._dict_parameters = parameters
        else:
            # this condition normally not reachable as the Insert
            # does not allow this construction to occur
            assert False, "This statement already has parameters"

    def _cant_mix_formats_error(self):
        raise exc.InvalidRequestError(
            "Can't mix single and multiple VALUES "
            "formats in one INSERT statement; one style appends to a "
            "list while the other replaces values, so the intent is "
            "ambiguous."
        )


@CompileState.plugin_for("default", "insert")
class InsertDMLState(DMLState):
    isinsert = True

    include_table_with_column_exprs = False

    def __init__(self, statement, compiler, **kw):
        self.statement = statement

        self.isinsert = True
        if statement._select_names:
            self._process_select_values(statement)
        if statement._values is not None:
            self._process_values(statement)
        if statement._multi_values:
            self._process_multi_values(statement)

    @util.memoized_property
    def _insert_col_keys(self):
        # this is also done in crud.py -> _key_getters_for_crud_column
        return [
            coercions.expect_as_key(roles.DMLColumnRole, col)
            for col in self._dict_parameters
        ]


@CompileState.plugin_for("default", "update")
class UpdateDMLState(DMLState):
    isupdate = True

    include_table_with_column_exprs = False

    def __init__(self, statement, compiler, **kw):
        self.statement = statement
        self.isupdate = True
        self._preserve_parameter_order = statement._preserve_parameter_order
        if statement._ordered_values is not None:
            self._process_ordered_values(statement)
        elif statement._values is not None:
            self._process_values(statement)
        elif statement._multi_values:
            self._process_multi_values(statement)
        self._extra_froms = ef = self._make_extra_froms(statement)
        self.is_multitable = mt = ef and self._dict_parameters
        self.include_table_with_column_exprs = (
            mt and compiler.render_table_with_column_in_update_from
        )


@CompileState.plugin_for("default", "delete")
class DeleteDMLState(DMLState):
    isdelete = True

    def __init__(self, statement, compiler, **kw):
        self.statement = statement

        self.isdelete = True
        self._extra_froms = self._make_extra_froms(statement)


class UpdateBase(
    roles.DMLRole,
    HasCTE,
    HasCompileState,
    DialectKWArgs,
    HasPrefixes,
    ReturnsRows,
    Executable,
    ClauseElement,
):
    """Form the base for ``INSERT``, ``UPDATE``, and ``DELETE`` statements."""

    __visit_name__ = "update_base"

    _execution_options = Executable._execution_options.union(
        {"autocommit": True}
    )
    _hints = util.immutabledict()
    named_with_column = False

    _return_defaults = False
    _return_defaults_columns = None
    _returning = ()

    is_dml = True

    @classmethod
    def _constructor_20_deprecations(cls, fn_name, clsname, names):

        param_to_method_lookup = dict(
            whereclause=(
                "The :paramref:`%(func)s.whereclause` parameter "
                "will be removed "
                "in SQLAlchemy 2.0.  Please refer to the "
                ":meth:`%(classname)s.where` method."
            ),
            values=(
                "The :paramref:`%(func)s.values` parameter will be removed "
                "in SQLAlchemy 2.0.  Please refer to the "
                ":meth:`%(classname)s.values` method."
            ),
            bind=(
                "The :paramref:`%(func)s.bind` parameter will be removed in "
                "SQLAlchemy 2.0.  Please use explicit connection execution."
            ),
            inline=(
                "The :paramref:`%(func)s.inline` parameter will be "
                "removed in "
                "SQLAlchemy 2.0.  Please use the "
                ":meth:`%(classname)s.inline` method."
            ),
            prefixes=(
                "The :paramref:`%(func)s.prefixes parameter will be "
                "removed in "
                "SQLAlchemy 2.0.  Please use the "
                ":meth:`%(classname)s.prefix_with` "
                "method."
            ),
            return_defaults=(
                "The :paramref:`%(func)s.return_defaults` parameter will be "
                "removed in SQLAlchemy 2.0.  Please use the "
                ":meth:`%(classname)s.return_defaults` method."
            ),
            returning=(
                "The :paramref:`%(func)s.returning` parameter will be "
                "removed in SQLAlchemy 2.0.  Please use the "
                ":meth:`%(classname)s.returning`` method."
            ),
            preserve_parameter_order=(
                "The :paramref:`%(func)s.preserve_parameter_order` parameter "
                "will be removed in SQLAlchemy 2.0.   Use the "
                ":meth:`%(classname)s.ordered_values` method with a list "
                "of tuples. "
            ),
        )

        return util.deprecated_params(
            **{
                name: (
                    "2.0",
                    param_to_method_lookup[name]
                    % {
                        "func": "_expression.%s" % fn_name,
                        "classname": "_expression.%s" % clsname,
                    },
                )
                for name in names
            }
        )

    def _generate_fromclause_column_proxies(self, fromclause):
        fromclause._columns._populate_separate_keys(
            col._make_proxy(fromclause) for col in self._returning
        )

    def params(self, *arg, **kw):
        """Set the parameters for the statement.

        This method raises ``NotImplementedError`` on the base class,
        and is overridden by :class:`.ValuesBase` to provide the
        SET/VALUES clause of UPDATE and INSERT.

        """
        raise NotImplementedError(
            "params() is not supported for INSERT/UPDATE/DELETE statements."
            " To set the values for an INSERT or UPDATE statement, use"
            " stmt.values(**parameters)."
        )

    @_generative
    def with_dialect_options(self, **opt):
        """Add dialect options to this INSERT/UPDATE/DELETE object.

        e.g.::

            upd = table.update().dialect_options(mysql_limit=10)

        .. versionadded: 1.4 - this method supersedes the dialect options
           associated with the constructor.


        """
        self._validate_dialect_kwargs(opt)

    def _validate_dialect_kwargs_deprecated(self, dialect_kw):
        util.warn_deprecated_20(
            "Passing dialect keyword arguments directly to the "
            "%s constructor is deprecated and will be removed in SQLAlchemy "
            "2.0.  Please use the ``with_dialect_options()`` method."
            % (self.__class__.__name__)
        )
        self._validate_dialect_kwargs(dialect_kw)

    def bind(self):
        """Return a 'bind' linked to this :class:`.UpdateBase`
        or a :class:`_schema.Table` associated with it.

        """
        return self._bind or self.table.bind

    def _set_bind(self, bind):
        self._bind = bind

    bind = property(bind, _set_bind)

    @_generative
    def returning(self, *cols):
        r"""Add a :term:`RETURNING` or equivalent clause to this statement.

        e.g.:

        .. sourcecode:: pycon+sql

            >>> stmt = (
            ...     table.update()
            ...     .where(table.c.data == "value")
            ...     .values(status="X")
            ...     .returning(table.c.server_flag, table.c.updated_timestamp)
            ... )
            >>> print(stmt)
            UPDATE some_table SET status=:status
            WHERE some_table.data = :data_1
            RETURNING some_table.server_flag, some_table.updated_timestamp

        The method may be invoked multiple times to add new entries to the
        list of expressions to be returned.

        .. versionadded:: 1.4.0b2 The method may be invoked multiple times to
         add new entries to the list of expressions to be returned.

        The given collection of column expressions should be derived from the
        table that is the target of the INSERT, UPDATE, or DELETE.  While
        :class:`_schema.Column` objects are typical, the elements can also be
        expressions:

        .. sourcecode:: pycon+sql

            >>> stmt = table.insert().returning(
            ...     (table.c.first_name + " " + table.c.last_name).label("fullname")
            ... )
            >>> print(stmt)
            INSERT INTO some_table (first_name, last_name)
            VALUES (:first_name, :last_name)
            RETURNING some_table.first_name || :first_name_1 || some_table.last_name AS fullname

        Upon compilation, a RETURNING clause, or database equivalent,
        will be rendered within the statement.   For INSERT and UPDATE,
        the values are the newly inserted/updated values.  For DELETE,
        the values are those of the rows which were deleted.

        Upon execution, the values of the columns to be returned are made
        available via the result set and can be iterated using
        :meth:`_engine.CursorResult.fetchone` and similar.
        For DBAPIs which do not
        natively support returning values (i.e. cx_oracle), SQLAlchemy will
        approximate this behavior at the result level so that a reasonable
        amount of behavioral neutrality is provided.

        Note that not all databases/DBAPIs
        support RETURNING.   For those backends with no support,
        an exception is raised upon compilation and/or execution.
        For those who do support it, the functionality across backends
        varies greatly, including restrictions on executemany()
        and other statements which return multiple rows. Please
        read the documentation notes for the database in use in
        order to determine the availability of RETURNING.

        .. seealso::

          :meth:`.ValuesBase.return_defaults` - an alternative method tailored
          towards efficient fetching of server-side defaults and triggers
          for single-row INSERTs or UPDATEs.

          :ref:`tutorial_insert_returning` - in the :ref:`unified_tutorial`

        """  # noqa: E501
        if self._return_defaults:
            raise exc.InvalidRequestError(
                "return_defaults() is already configured on this statement"
            )
        self._returning += tuple(
            coercions.expect(roles.ColumnsClauseRole, c) for c in cols
        )

    @property
    def _all_selected_columns(self):
        return self._returning

    @property
    def exported_columns(self):
        """Return the RETURNING columns as a column collection for this
        statement.

        .. versionadded:: 1.4

        """
        # TODO: no coverage here
        return ColumnCollection(
            (c.key, c) for c in self._all_selected_columns
        ).as_immutable()

    @_generative
    def with_hint(self, text, selectable=None, dialect_name="*"):
        """Add a table hint for a single table to this
        INSERT/UPDATE/DELETE statement.

        .. note::

         :meth:`.UpdateBase.with_hint` currently applies only to
         Microsoft SQL Server.  For MySQL INSERT/UPDATE/DELETE hints, use
         :meth:`.UpdateBase.prefix_with`.

        The text of the hint is rendered in the appropriate
        location for the database backend in use, relative
        to the :class:`_schema.Table` that is the subject of this
        statement, or optionally to that of the given
        :class:`_schema.Table` passed as the ``selectable`` argument.

        The ``dialect_name`` option will limit the rendering of a particular
        hint to a particular backend. Such as, to add a hint
        that only takes effect for SQL Server::

            mytable.insert().with_hint("WITH (PAGLOCK)", dialect_name="mssql")

        :param text: Text of the hint.
        :param selectable: optional :class:`_schema.Table` that specifies
         an element of the FROM clause within an UPDATE or DELETE
         to be the subject of the hint - applies only to certain backends.
        :param dialect_name: defaults to ``*``, if specified as the name
         of a particular dialect, will apply these hints only when
         that dialect is in use.
        """
        if selectable is None:
            selectable = self.table

        self._hints = self._hints.union({(selectable, dialect_name): text})

    @property
    def entity_description(self):
        """Return a :term:`plugin-enabled` description of the table and/or
        entity which this DML construct is operating against.

        This attribute is generally useful when using the ORM, as an
        extended structure which includes information about mapped
        entities is returned.  The section :ref:`queryguide_inspection`
        contains more background.

        For a Core statement, the structure returned by this accessor
        is derived from the :attr:`.UpdateBase.table` attribute, and
        refers to the :class:`.Table` being inserted, updated, or deleted::

            >>> stmt = insert(user_table)
            >>> stmt.entity_description
            {
                "name": "user_table",
                "table": Table("user_table", ...)
            }

        .. versionadded:: 1.4.33

        .. seealso::

            :attr:`.UpdateBase.returning_column_descriptions`

            :attr:`.Select.column_descriptions` - entity information for
            a :func:`.select` construct

            :ref:`queryguide_inspection` - ORM background

        """
        meth = DMLState.get_plugin_class(self).get_entity_description
        return meth(self)

    @property
    def returning_column_descriptions(self):
        """Return a :term:`plugin-enabled` description of the columns
        which this DML construct is RETURNING against, in other words
        the expressions established as part of :meth:`.UpdateBase.returning`.

        This attribute is generally useful when using the ORM, as an
        extended structure which includes information about mapped
        entities is returned.  The section :ref:`queryguide_inspection`
        contains more background.

        For a Core statement, the structure returned by this accessor is
        derived from the same objects that are returned by the
        :attr:`.UpdateBase.exported_columns` accessor::

            >>> stmt = insert(user_table).returning(user_table.c.id, user_table.c.name)
            >>> stmt.entity_description
            [
                {
                    "name": "id",
                    "type": Integer,
                    "expr": Column("id", Integer(), table=<user>, ...)
                },
                {
                    "name": "name",
                    "type": String(),
                    "expr": Column("name", String(), table=<user>, ...)
                },
            ]

        .. versionadded:: 1.4.33

        .. seealso::

            :attr:`.UpdateBase.entity_description`

            :attr:`.Select.column_descriptions` - entity information for
            a :func:`.select` construct

            :ref:`queryguide_inspection` - ORM background

        """  # noqa: E501
        meth = DMLState.get_plugin_class(
            self
        ).get_returning_column_descriptions
        return meth(self)


class ValuesBase(UpdateBase):
    """Supplies support for :meth:`.ValuesBase.values` to
    INSERT and UPDATE constructs."""

    __visit_name__ = "values_base"

    _supports_multi_parameters = False
    _preserve_parameter_order = False
    select = None
    _post_values_clause = None

    _values = None
    _multi_values = ()
    _ordered_values = None
    _select_names = None

    _returning = ()

    def __init__(self, table, values, prefixes):
        self.table = coercions.expect(
            roles.DMLTableRole, table, apply_propagate_attrs=self
        )
        if values is not None:
            self.values.non_generative(self, values)
        if prefixes:
            self._setup_prefixes(prefixes)

    @_generative
    @_exclusive_against(
        "_select_names",
        "_ordered_values",
        msgs={
            "_select_names": "This construct already inserts from a SELECT",
            "_ordered_values": "This statement already has ordered "
            "values present",
        },
    )
    def values(self, *args, **kwargs):
        r"""Specify a fixed VALUES clause for an INSERT statement, or the SET
        clause for an UPDATE.

        Note that the :class:`_expression.Insert` and
        :class:`_expression.Update`
        constructs support
        per-execution time formatting of the VALUES and/or SET clauses,
        based on the arguments passed to :meth:`_engine.Connection.execute`.
        However, the :meth:`.ValuesBase.values` method can be used to "fix" a
        particular set of parameters into the statement.

        Multiple calls to :meth:`.ValuesBase.values` will produce a new
        construct, each one with the parameter list modified to include
        the new parameters sent.  In the typical case of a single
        dictionary of parameters, the newly passed keys will replace
        the same keys in the previous construct.  In the case of a list-based
        "multiple values" construct, each new list of values is extended
        onto the existing list of values.

        :param \**kwargs: key value pairs representing the string key
          of a :class:`_schema.Column`
          mapped to the value to be rendered into the
          VALUES or SET clause::

                users.insert().values(name="some name")

                users.update().where(users.c.id==5).values(name="some name")

        :param \*args: As an alternative to passing key/value parameters,
         a dictionary, tuple, or list of dictionaries or tuples can be passed
         as a single positional argument in order to form the VALUES or
         SET clause of the statement.  The forms that are accepted vary
         based on whether this is an :class:`_expression.Insert` or an
         :class:`_expression.Update` construct.

         For either an :class:`_expression.Insert` or
         :class:`_expression.Update`
         construct, a single dictionary can be passed, which works the same as
         that of the kwargs form::

            users.insert().values({"name": "some name"})

            users.update().values({"name": "some new name"})

         Also for either form but more typically for the
         :class:`_expression.Insert` construct, a tuple that contains an
         entry for every column in the table is also accepted::

            users.insert().values((5, "some name"))

         The :class:`_expression.Insert` construct also supports being
         passed a list of dictionaries or full-table-tuples, which on the
         server will render the less common SQL syntax of "multiple values" -
         this syntax is supported on backends such as SQLite, PostgreSQL,
         MySQL, but not necessarily others::

            users.insert().values([
                                {"name": "some name"},
                                {"name": "some other name"},
                                {"name": "yet another name"},
                            ])

         The above form would render a multiple VALUES statement similar to::

                INSERT INTO users (name) VALUES
                                (:name_1),
                                (:name_2),
                                (:name_3)

         It is essential to note that **passing multiple values is
         NOT the same as using traditional executemany() form**.  The above
         syntax is a **special** syntax not typically used.  To emit an
         INSERT statement against multiple rows, the normal method is
         to pass a multiple values list to the
         :meth:`_engine.Connection.execute`
         method, which is supported by all database backends and is generally
         more efficient for a very large number of parameters.

           .. seealso::

               :ref:`tutorial_multiple_parameters` - an introduction to
               the traditional Core method of multiple parameter set
               invocation for INSERTs and other statements.

           .. versionchanged:: 1.0.0 an INSERT that uses a multiple-VALUES
              clause, even a list of length one,
              implies that the :paramref:`_expression.Insert.inline`
              flag is set to
              True, indicating that the statement will not attempt to fetch
              the "last inserted primary key" or other defaults.  The
              statement deals with an arbitrary number of rows, so the
              :attr:`_engine.CursorResult.inserted_primary_key`
              accessor does not
              apply.

           .. versionchanged:: 1.0.0 A multiple-VALUES INSERT now supports
              columns with Python side default values and callables in the
              same way as that of an "executemany" style of invocation; the
              callable is invoked for each row.   See :ref:`bug_3288`
              for other details.

          The UPDATE construct also supports rendering the SET parameters
          in a specific order.  For this feature refer to the
          :meth:`_expression.Update.ordered_values` method.

           .. seealso::

              :meth:`_expression.Update.ordered_values`


        """
        if args:
            # positional case.  this is currently expensive.   we don't
            # yet have positional-only args so we have to check the length.
            # then we need to check multiparams vs. single dictionary.
            # since the parameter format is needed in order to determine
            # a cache key, we need to determine this up front.
            arg = args[0]

            if kwargs:
                raise exc.ArgumentError(
                    "Can't pass positional and kwargs to values() "
                    "simultaneously"
                )
            elif len(args) > 1:
                raise exc.ArgumentError(
                    "Only a single dictionary/tuple or list of "
                    "dictionaries/tuples is accepted positionally."
                )

            elif not self._preserve_parameter_order and isinstance(
                arg, collections_abc.Sequence
            ):

                if arg and isinstance(arg[0], (list, dict, tuple)):
                    self._multi_values += (arg,)
                    return

                # tuple values
                arg = {c.key: value for c, value in zip(self.table.c, arg)}
            elif self._preserve_parameter_order and not isinstance(
                arg, collections_abc.Sequence
            ):
                raise ValueError(
                    "When preserve_parameter_order is True, "
                    "values() only accepts a list of 2-tuples"
                )

        else:
            # kwarg path.  this is the most common path for non-multi-params
            # so this is fairly quick.
            arg = kwargs
            if args:
                raise exc.ArgumentError(
                    "Only a single dictionary/tuple or list of "
                    "dictionaries/tuples is accepted positionally."
                )

        # for top level values(), convert literals to anonymous bound
        # parameters at statement construction time, so that these values can
        # participate in the cache key process like any other ClauseElement.
        # crud.py now intercepts bound parameters with unique=True from here
        # and ensures they get the "crud"-style name when rendered.

        kv_generator = DMLState.get_plugin_class(self)._get_crud_kv_pairs

        if self._preserve_parameter_order:
            self._ordered_values = kv_generator(self, arg)
        else:
            arg = {k: v for k, v in kv_generator(self, arg.items())}
            if self._values:
                self._values = self._values.union(arg)
            else:
                self._values = util.immutabledict(arg)

    @_generative
    @_exclusive_against(
        "_returning",
        msgs={
            "_returning": "RETURNING is already configured on this statement"
        },
        defaults={"_returning": _returning},
    )
    def return_defaults(self, *cols):
        """Make use of a :term:`RETURNING` clause for the purpose
        of fetching server-side expressions and defaults.

        E.g.::

            stmt = table.insert().values(data='newdata').return_defaults()

            result = connection.execute(stmt)

            server_created_at = result.returned_defaults['created_at']

        When used against a backend that supports RETURNING, all column
        values generated by SQL expression or server-side-default will be
        added to any existing RETURNING clause, provided that
        :meth:`.UpdateBase.returning` is not used simultaneously.  The column
        values will then be available on the result using the
        :attr:`_engine.CursorResult.returned_defaults` accessor as
        a dictionary,
        referring to values keyed to the :class:`_schema.Column`
        object as well as
        its ``.key``.

        This method differs from :meth:`.UpdateBase.returning` in these ways:

        1. :meth:`.ValuesBase.return_defaults` is only intended for use with an
           INSERT or an UPDATE statement that matches exactly one row per
           parameter set. While the RETURNING construct in the general sense
           supports multiple rows for a multi-row UPDATE or DELETE statement,
           or for special cases of INSERT that return multiple rows (e.g.
           INSERT from SELECT, multi-valued VALUES clause),
           :meth:`.ValuesBase.return_defaults` is intended only for an
           "ORM-style" single-row INSERT/UPDATE statement.  The row
           returned by the statement is also consumed implicitly when
           :meth:`.ValuesBase.return_defaults` is used.  By contrast,
           :meth:`.UpdateBase.returning` leaves the RETURNING result-set intact
           with a collection of any number of rows.

        2. It is compatible with the existing logic to fetch auto-generated
           primary key values, also known as "implicit returning".  Backends
           that support RETURNING will automatically make use of RETURNING in
           order to fetch the value of newly generated primary keys; while the
           :meth:`.UpdateBase.returning` method circumvents this behavior,
           :meth:`.ValuesBase.return_defaults` leaves it intact.

        3. It can be called against any backend.  Backends that don't support
           RETURNING will skip the usage of the feature, rather than raising
           an exception.  The return value of
           :attr:`_engine.CursorResult.returned_defaults` will be ``None``

        4. An INSERT statement invoked with executemany() is supported if the
           backend database driver supports the
           ``insert_executemany_returning`` feature, currently this includes
           PostgreSQL with psycopg2.  When executemany is used, the
           :attr:`_engine.CursorResult.returned_defaults_rows` and
           :attr:`_engine.CursorResult.inserted_primary_key_rows` accessors
           will return the inserted defaults and primary keys.

           .. versionadded:: 1.4

        :meth:`.ValuesBase.return_defaults` is used by the ORM to provide
        an efficient implementation for the ``eager_defaults`` feature of
        :func:`.mapper`.

        :param cols: optional list of column key names or
         :class:`_schema.Column`
         objects.  If omitted, all column expressions evaluated on the server
         are added to the returning list.

        .. versionadded:: 0.9.0

        .. seealso::

            :meth:`.UpdateBase.returning`

            :attr:`_engine.CursorResult.returned_defaults`

            :attr:`_engine.CursorResult.returned_defaults_rows`

            :attr:`_engine.CursorResult.inserted_primary_key`

            :attr:`_engine.CursorResult.inserted_primary_key_rows`

        """
        self._return_defaults = True
        self._return_defaults_columns = cols


class Insert(ValuesBase):
    """Represent an INSERT construct.

    The :class:`_expression.Insert` object is created using the
    :func:`_expression.insert()` function.

    """

    __visit_name__ = "insert"

    _supports_multi_parameters = True

    select = None
    include_insert_from_select_defaults = False

    is_insert = True

    _traverse_internals = (
        [
            ("table", InternalTraversal.dp_clauseelement),
            ("_inline", InternalTraversal.dp_boolean),
            ("_select_names", InternalTraversal.dp_string_list),
            ("_values", InternalTraversal.dp_dml_values),
            ("_multi_values", InternalTraversal.dp_dml_multi_values),
            ("select", InternalTraversal.dp_clauseelement),
            ("_post_values_clause", InternalTraversal.dp_clauseelement),
            ("_returning", InternalTraversal.dp_clauseelement_list),
            ("_hints", InternalTraversal.dp_table_hint_list),
            ("_return_defaults", InternalTraversal.dp_boolean),
            (
                "_return_defaults_columns",
                InternalTraversal.dp_clauseelement_list,
            ),
        ]
        + HasPrefixes._has_prefixes_traverse_internals
        + DialectKWArgs._dialect_kwargs_traverse_internals
        + Executable._executable_traverse_internals
        + HasCTE._has_ctes_traverse_internals
    )

    @ValuesBase._constructor_20_deprecations(
        "insert",
        "Insert",
        [
            "values",
            "inline",
            "bind",
            "prefixes",
            "returning",
            "return_defaults",
        ],
    )
    def __init__(
        self,
        table,
        values=None,
        inline=False,
        bind=None,
        prefixes=None,
        returning=None,
        return_defaults=False,
        **dialect_kw
    ):
        """Construct an :class:`_expression.Insert` object.

        E.g.::

            from sqlalchemy import insert

            stmt = (
                insert(user_table).
                values(name='username', fullname='Full Username')
            )

        Similar functionality is available via the
        :meth:`_expression.TableClause.insert` method on
        :class:`_schema.Table`.

        .. seealso::

            :ref:`tutorial_core_insert` - in the :ref:`unified_tutorial`


        :param table: :class:`_expression.TableClause`
         which is the subject of the
         insert.

        :param values: collection of values to be inserted; see
         :meth:`_expression.Insert.values`
         for a description of allowed formats here.
         Can be omitted entirely; a :class:`_expression.Insert` construct
         will also dynamically render the VALUES clause at execution time
         based on the parameters passed to :meth:`_engine.Connection.execute`.

        :param inline: if True, no attempt will be made to retrieve the
         SQL-generated default values to be provided within the statement;
         in particular,
         this allows SQL expressions to be rendered 'inline' within the
         statement without the need to pre-execute them beforehand; for
         backends that support "returning", this turns off the "implicit
         returning" feature for the statement.

        If both :paramref:`_expression.Insert.values` and compile-time bind
        parameters are present, the compile-time bind parameters override the
        information specified within :paramref:`_expression.Insert.values` on a
        per-key basis.

        The keys within :paramref:`_expression.Insert.values` can be either
        :class:`~sqlalchemy.schema.Column` objects or their string
        identifiers. Each key may reference one of:

        * a literal data value (i.e. string, number, etc.);
        * a Column object;
        * a SELECT statement.

        If a ``SELECT`` statement is specified which references this
        ``INSERT`` statement's table, the statement will be correlated
        against the ``INSERT`` statement.

        .. seealso::

            :ref:`tutorial_core_insert` - in the :ref:`unified_tutorial`

        """
        super(Insert, self).__init__(table, values, prefixes)
        self._bind = bind
        self._inline = inline
        if returning:
            self._returning = returning
        if dialect_kw:
            self._validate_dialect_kwargs_deprecated(dialect_kw)

        if return_defaults:
            self._return_defaults = True
            if not isinstance(return_defaults, bool):
                self._return_defaults_columns = return_defaults

    @_generative
    def inline(self):
        """Make this :class:`_expression.Insert` construct "inline" .

        When set, no attempt will be made to retrieve the
        SQL-generated default values to be provided within the statement;
        in particular,
        this allows SQL expressions to be rendered 'inline' within the
        statement without the need to pre-execute them beforehand; for
        backends that support "returning", this turns off the "implicit
        returning" feature for the statement.


        .. versionchanged:: 1.4 the :paramref:`_expression.Insert.inline`
           parameter
           is now superseded by the :meth:`_expression.Insert.inline` method.

        """
        self._inline = True

    @_generative
    def from_select(self, names, select, include_defaults=True):
        """Return a new :class:`_expression.Insert` construct which represents
        an ``INSERT...FROM SELECT`` statement.

        e.g.::

            sel = select(table1.c.a, table1.c.b).where(table1.c.c > 5)
            ins = table2.insert().from_select(['a', 'b'], sel)

        :param names: a sequence of string column names or
         :class:`_schema.Column`
         objects representing the target columns.
        :param select: a :func:`_expression.select` construct,
         :class:`_expression.FromClause`
         or other construct which resolves into a
         :class:`_expression.FromClause`,
         such as an ORM :class:`_query.Query` object, etc.  The order of
         columns returned from this FROM clause should correspond to the
         order of columns sent as the ``names`` parameter;  while this
         is not checked before passing along to the database, the database
         would normally raise an exception if these column lists don't
         correspond.
        :param include_defaults: if True, non-server default values and
         SQL expressions as specified on :class:`_schema.Column` objects
         (as documented in :ref:`metadata_defaults_toplevel`) not
         otherwise specified in the list of names will be rendered
         into the INSERT and SELECT statements, so that these values are also
         included in the data to be inserted.

         .. note:: A Python-side default that uses a Python callable function
            will only be invoked **once** for the whole statement, and **not
            per row**.

         .. versionadded:: 1.0.0 - :meth:`_expression.Insert.from_select`
            now renders
            Python-side and SQL expression column defaults into the
            SELECT statement for columns otherwise not included in the
            list of column names.

        .. versionchanged:: 1.0.0 an INSERT that uses FROM SELECT
           implies that the :paramref:`_expression.insert.inline`
           flag is set to
           True, indicating that the statement will not attempt to fetch
           the "last inserted primary key" or other defaults.  The statement
           deals with an arbitrary number of rows, so the
           :attr:`_engine.CursorResult.inserted_primary_key`
           accessor does not apply.

        """

        if self._values:
            raise exc.InvalidRequestError(
                "This construct already inserts value expressions"
            )

        self._select_names = names
        self._inline = True
        self.include_insert_from_select_defaults = include_defaults
        self.select = coercions.expect(roles.DMLSelectRole, select)


class DMLWhereBase(object):
    _where_criteria = ()

    @_generative
    def where(self, *whereclause):
        """Return a new construct with the given expression(s) added to
        its WHERE clause, joined to the existing clause via AND, if any.

        Both :meth:`_dml.Update.where` and :meth:`_dml.Delete.where`
        support multiple-table forms, including database-specific
        ``UPDATE...FROM`` as well as ``DELETE..USING``.  For backends that
        don't have multiple-table support, a backend agnostic approach
        to using multiple tables is to make use of correlated subqueries.
        See the linked tutorial sections below for examples.

        .. seealso::

            :ref:`tutorial_correlated_updates`

            :ref:`tutorial_update_from`

            :ref:`tutorial_multi_table_deletes`

        """

        for criterion in whereclause:
            where_criteria = coercions.expect(roles.WhereHavingRole, criterion)
            self._where_criteria += (where_criteria,)

    def filter(self, *criteria):
        """A synonym for the :meth:`_dml.DMLWhereBase.where` method.

        .. versionadded:: 1.4

        """

        return self.where(*criteria)

    def _filter_by_zero(self):
        return self.table

    def filter_by(self, **kwargs):
        r"""apply the given filtering criterion as a WHERE clause
        to this select.

        """
        from_entity = self._filter_by_zero()

        clauses = [
            _entity_namespace_key(from_entity, key) == value
            for key, value in kwargs.items()
        ]
        return self.filter(*clauses)

    @property
    def whereclause(self):
        """Return the completed WHERE clause for this :class:`.DMLWhereBase`
        statement.

        This assembles the current collection of WHERE criteria
        into a single :class:`_expression.BooleanClauseList` construct.


        .. versionadded:: 1.4

        """

        return BooleanClauseList._construct_for_whereclause(
            self._where_criteria
        )


class Update(DMLWhereBase, ValuesBase):
    """Represent an Update construct.

    The :class:`_expression.Update` object is created using the
    :func:`_expression.update()` function.

    """

    __visit_name__ = "update"

    is_update = True

    _traverse_internals = (
        [
            ("table", InternalTraversal.dp_clauseelement),
            ("_where_criteria", InternalTraversal.dp_clauseelement_list),
            ("_inline", InternalTraversal.dp_boolean),
            ("_ordered_values", InternalTraversal.dp_dml_ordered_values),
            ("_values", InternalTraversal.dp_dml_values),
            ("_returning", InternalTraversal.dp_clauseelement_list),
            ("_hints", InternalTraversal.dp_table_hint_list),
            ("_return_defaults", InternalTraversal.dp_boolean),
            (
                "_return_defaults_columns",
                InternalTraversal.dp_clauseelement_list,
            ),
        ]
        + HasPrefixes._has_prefixes_traverse_internals
        + DialectKWArgs._dialect_kwargs_traverse_internals
        + Executable._executable_traverse_internals
        + HasCTE._has_ctes_traverse_internals
    )

    @ValuesBase._constructor_20_deprecations(
        "update",
        "Update",
        [
            "whereclause",
            "values",
            "inline",
            "bind",
            "prefixes",
            "returning",
            "return_defaults",
            "preserve_parameter_order",
        ],
    )
    def __init__(
        self,
        table,
        whereclause=None,
        values=None,
        inline=False,
        bind=None,
        prefixes=None,
        returning=None,
        return_defaults=False,
        preserve_parameter_order=False,
        **dialect_kw
    ):
        r"""Construct an :class:`_expression.Update` object.

        E.g.::

            from sqlalchemy import update

            stmt = (
                update(user_table).
                where(user_table.c.id == 5).
                values(name='user #5')
            )

        Similar functionality is available via the
        :meth:`_expression.TableClause.update` method on
        :class:`_schema.Table`.

        :param table: A :class:`_schema.Table`
         object representing the database
         table to be updated.

        :param whereclause: Optional SQL expression describing the ``WHERE``
         condition of the ``UPDATE`` statement; is equivalent to using the
         more modern :meth:`~Update.where()` method to specify the ``WHERE``
         clause.

        :param values:
          Optional dictionary which specifies the ``SET`` conditions of the
          ``UPDATE``.  If left as ``None``, the ``SET``
          conditions are determined from those parameters passed to the
          statement during the execution and/or compilation of the
          statement.   When compiled standalone without any parameters,
          the ``SET`` clause generates for all columns.

          Modern applications may prefer to use the generative
          :meth:`_expression.Update.values` method to set the values of the
          UPDATE statement.

        :param inline:
          if True, SQL defaults present on :class:`_schema.Column` objects via
          the ``default`` keyword will be compiled 'inline' into the statement
          and not pre-executed.  This means that their values will not
          be available in the dictionary returned from
          :meth:`_engine.CursorResult.last_updated_params`.

        :param preserve_parameter_order: if True, the update statement is
          expected to receive parameters **only** via the
          :meth:`_expression.Update.values` method,
          and they must be passed as a Python
          ``list`` of 2-tuples. The rendered UPDATE statement will emit the SET
          clause for each referenced column maintaining this order.

          .. versionadded:: 1.0.10

          .. seealso::

            :ref:`updates_order_parameters` - illustrates the
            :meth:`_expression.Update.ordered_values` method.

        If both ``values`` and compile-time bind parameters are present, the
        compile-time bind parameters override the information specified
        within ``values`` on a per-key basis.

        The keys within ``values`` can be either :class:`_schema.Column`
        objects or their string identifiers (specifically the "key" of the
        :class:`_schema.Column`, normally but not necessarily equivalent to
        its "name").  Normally, the
        :class:`_schema.Column` objects used here are expected to be
        part of the target :class:`_schema.Table` that is the table
        to be updated.  However when using MySQL, a multiple-table
        UPDATE statement can refer to columns from any of
        the tables referred to in the WHERE clause.

        The values referred to in ``values`` are typically:

        * a literal data value (i.e. string, number, etc.)
        * a SQL expression, such as a related :class:`_schema.Column`,
          a scalar-returning :func:`_expression.select` construct,
          etc.

        When combining :func:`_expression.select` constructs within the
        values clause of an :func:`_expression.update`
        construct, the subquery represented
        by the :func:`_expression.select` should be *correlated* to the
        parent table, that is, providing criterion which links the table inside
        the subquery to the outer table being updated::

            users.update().values(
                    name=select(addresses.c.email_address).\
                            where(addresses.c.user_id==users.c.id).\
                            scalar_subquery()
                )

        .. seealso::

            :ref:`inserts_and_updates` - SQL Expression
            Language Tutorial


        """
        self._preserve_parameter_order = preserve_parameter_order
        super(Update, self).__init__(table, values, prefixes)
        self._bind = bind
        if returning:
            self._returning = returning
        if whereclause is not None:
            self._where_criteria += (
                coercions.expect(roles.WhereHavingRole, whereclause),
            )
        self._inline = inline
        if dialect_kw:
            self._validate_dialect_kwargs_deprecated(dialect_kw)
        self._return_defaults = return_defaults

    @_generative
    def ordered_values(self, *args):
        """Specify the VALUES clause of this UPDATE statement with an explicit
        parameter ordering that will be maintained in the SET clause of the
        resulting UPDATE statement.

        E.g.::

            stmt = table.update().ordered_values(
                ("name", "ed"), ("ident": "foo")
            )

        .. seealso::

           :ref:`tutorial_parameter_ordered_updates` - full example of the
           :meth:`_expression.Update.ordered_values` method.

        .. versionchanged:: 1.4 The :meth:`_expression.Update.ordered_values`
           method
           supersedes the
           :paramref:`_expression.update.preserve_parameter_order`
           parameter, which will be removed in SQLAlchemy 2.0.

        """
        if self._values:
            raise exc.ArgumentError(
                "This statement already has values present"
            )
        elif self._ordered_values:
            raise exc.ArgumentError(
                "This statement already has ordered values present"
            )

        kv_generator = DMLState.get_plugin_class(self)._get_crud_kv_pairs
        self._ordered_values = kv_generator(self, args)

    @_generative
    def inline(self):
        """Make this :class:`_expression.Update` construct "inline" .

        When set, SQL defaults present on :class:`_schema.Column`
        objects via the
        ``default`` keyword will be compiled 'inline' into the statement and
        not pre-executed.  This means that their values will not be available
        in the dictionary returned from
        :meth:`_engine.CursorResult.last_updated_params`.

        .. versionchanged:: 1.4 the :paramref:`_expression.update.inline`
           parameter
           is now superseded by the :meth:`_expression.Update.inline` method.

        """
        self._inline = True


class Delete(DMLWhereBase, UpdateBase):
    """Represent a DELETE construct.

    The :class:`_expression.Delete` object is created using the
    :func:`_expression.delete()` function.

    """

    __visit_name__ = "delete"

    is_delete = True

    _traverse_internals = (
        [
            ("table", InternalTraversal.dp_clauseelement),
            ("_where_criteria", InternalTraversal.dp_clauseelement_list),
            ("_returning", InternalTraversal.dp_clauseelement_list),
            ("_hints", InternalTraversal.dp_table_hint_list),
        ]
        + HasPrefixes._has_prefixes_traverse_internals
        + DialectKWArgs._dialect_kwargs_traverse_internals
        + Executable._executable_traverse_internals
        + HasCTE._has_ctes_traverse_internals
    )

    @ValuesBase._constructor_20_deprecations(
        "delete",
        "Delete",
        ["whereclause", "values", "bind", "prefixes", "returning"],
    )
    def __init__(
        self,
        table,
        whereclause=None,
        bind=None,
        returning=None,
        prefixes=None,
        **dialect_kw
    ):
        r"""Construct :class:`_expression.Delete` object.

        E.g.::

            from sqlalchemy import delete

            stmt = (
                delete(user_table).
                where(user_table.c.id == 5)
            )

        Similar functionality is available via the
        :meth:`_expression.TableClause.delete` method on
        :class:`_schema.Table`.

        .. seealso::

            :ref:`inserts_and_updates` - in the
            :ref:`1.x tutorial <sqlexpression_toplevel>`

            :ref:`tutorial_core_update_delete` - in the :ref:`unified_tutorial`


        :param table: The table to delete rows from.

        :param whereclause: Optional SQL expression describing the ``WHERE``
         condition of the ``DELETE`` statement; is equivalent to using the
         more modern :meth:`~Delete.where()` method to specify the ``WHERE``
         clause.

        .. seealso::

            :ref:`deletes` - SQL Expression Tutorial

        """
        self._bind = bind
        self.table = coercions.expect(
            roles.DMLTableRole, table, apply_propagate_attrs=self
        )
        if returning:
            self._returning = returning

        if prefixes:
            self._setup_prefixes(prefixes)

        if whereclause is not None:
            self._where_criteria += (
                coercions.expect(roles.WhereHavingRole, whereclause),
            )

        if dialect_kw:
            self._validate_dialect_kwargs_deprecated(dialect_kw)
