# orm/context.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php
import itertools

from . import attributes
from . import interfaces
from . import loading
from .base import _is_aliased_class
from .interfaces import ORMColumnsClauseRole
from .path_registry import PathRegistry
from .util import _entity_corresponds_to
from .util import _ORMJoin
from .util import aliased
from .util import Bundle
from .util import ORMAdapter
from .. import exc as sa_exc
from .. import future
from .. import inspect
from .. import sql
from .. import util
from ..sql import ClauseElement
from ..sql import coercions
from ..sql import expression
from ..sql import roles
from ..sql import util as sql_util
from ..sql import visitors
from ..sql.base import _entity_namespace_key
from ..sql.base import _select_iterables
from ..sql.base import CacheableOptions
from ..sql.base import CompileState
from ..sql.base import Options
from ..sql.selectable import LABEL_STYLE_DISAMBIGUATE_ONLY
from ..sql.selectable import LABEL_STYLE_NONE
from ..sql.selectable import LABEL_STYLE_TABLENAME_PLUS_COL
from ..sql.selectable import SelectState
from ..sql.visitors import ExtendedInternalTraversal
from ..sql.visitors import InternalTraversal

_path_registry = PathRegistry.root

_EMPTY_DICT = util.immutabledict()


LABEL_STYLE_LEGACY_ORM = util.symbol("LABEL_STYLE_LEGACY_ORM")


class QueryContext(object):
    __slots__ = (
        "compile_state",
        "query",
        "params",
        "load_options",
        "bind_arguments",
        "execution_options",
        "session",
        "autoflush",
        "populate_existing",
        "invoke_all_eagers",
        "version_check",
        "refresh_state",
        "create_eager_joins",
        "propagated_loader_options",
        "attributes",
        "runid",
        "partials",
        "post_load_paths",
        "identity_token",
        "yield_per",
        "loaders_require_buffering",
        "loaders_require_uniquing",
    )

    class default_load_options(Options):
        _only_return_tuples = False
        _populate_existing = False
        _version_check = False
        _invoke_all_eagers = True
        _autoflush = True
        _refresh_identity_token = None
        _yield_per = None
        _refresh_state = None
        _lazy_loaded_from = None
        _legacy_uniquing = False

    def __init__(
        self,
        compile_state,
        statement,
        params,
        session,
        load_options,
        execution_options=None,
        bind_arguments=None,
    ):
        self.load_options = load_options
        self.execution_options = execution_options or _EMPTY_DICT
        self.bind_arguments = bind_arguments or _EMPTY_DICT
        self.compile_state = compile_state
        self.query = statement
        self.session = session
        self.loaders_require_buffering = False
        self.loaders_require_uniquing = False
        self.params = params

        cached_options = compile_state.select_statement._with_options
        uncached_options = statement._with_options

        # see issue #7447 , #8399 for some background
        # propagated loader options will be present on loaded InstanceState
        # objects under state.load_options and are typically used by
        # LazyLoader to apply options to the SELECT statement it emits.
        # For compile state options (i.e. loader strategy options), these
        # need to line up with the ".load_path" attribute which in
        # loader.py is pulled from context.compile_state.current_path.
        # so, this means these options have to be the ones from the
        # *cached* statement that's travelling with compile_state, not the
        # *current* statement which won't match up for an ad-hoc
        # AliasedClass
        self.propagated_loader_options = tuple(
            opt._adapt_cached_option_to_uncached_option(self, uncached_opt)
            for opt, uncached_opt in zip(cached_options, uncached_options)
            if opt.propagate_to_loaders
        )

        self.attributes = dict(compile_state.attributes)

        self.autoflush = load_options._autoflush
        self.populate_existing = load_options._populate_existing
        self.invoke_all_eagers = load_options._invoke_all_eagers
        self.version_check = load_options._version_check
        self.refresh_state = load_options._refresh_state
        self.yield_per = load_options._yield_per
        self.identity_token = load_options._refresh_identity_token

        if self.yield_per and compile_state._no_yield_pers:
            raise sa_exc.InvalidRequestError(
                "The yield_per Query option is currently not "
                "compatible with %s eager loading.  Please "
                "specify lazyload('*') or query.enable_eagerloads(False) in "
                "order to "
                "proceed with query.yield_per()."
                % ", ".join(compile_state._no_yield_pers)
            )


_orm_load_exec_options = util.immutabledict(
    {"_result_disable_adapt_to_context": True, "future_result": True}
)


class ORMCompileState(CompileState):
    # note this is a dictionary, but the
    # default_compile_options._with_polymorphic_adapt_map is a tuple
    _with_polymorphic_adapt_map = _EMPTY_DICT

    class default_compile_options(CacheableOptions):
        _cache_key_traversal = [
            ("_use_legacy_query_style", InternalTraversal.dp_boolean),
            ("_for_statement", InternalTraversal.dp_boolean),
            ("_bake_ok", InternalTraversal.dp_boolean),
            (
                "_with_polymorphic_adapt_map",
                ExtendedInternalTraversal.dp_has_cache_key_tuples,
            ),
            ("_current_path", InternalTraversal.dp_has_cache_key),
            ("_enable_single_crit", InternalTraversal.dp_boolean),
            ("_enable_eagerloads", InternalTraversal.dp_boolean),
            ("_orm_only_from_obj_alias", InternalTraversal.dp_boolean),
            ("_only_load_props", InternalTraversal.dp_plain_obj),
            ("_set_base_alias", InternalTraversal.dp_boolean),
            ("_for_refresh_state", InternalTraversal.dp_boolean),
            ("_render_for_subquery", InternalTraversal.dp_boolean),
            ("_is_star", InternalTraversal.dp_boolean),
        ]

        # set to True by default from Query._statement_20(), to indicate
        # the rendered query should look like a legacy ORM query.  right
        # now this basically indicates we should use tablename_columnname
        # style labels.    Generally indicates the statement originated
        # from a Query object.
        _use_legacy_query_style = False

        # set *only* when we are coming from the Query.statement
        # accessor, or a Query-level equivalent such as
        # query.subquery().  this supersedes "toplevel".
        _for_statement = False

        _bake_ok = True
        _with_polymorphic_adapt_map = ()
        _current_path = _path_registry
        _enable_single_crit = True
        _enable_eagerloads = True
        _orm_only_from_obj_alias = True
        _only_load_props = None
        _set_base_alias = False
        _for_refresh_state = False
        _render_for_subquery = False
        _is_star = False

    current_path = _path_registry

    def __init__(self, *arg, **kw):
        raise NotImplementedError()

    def _append_dedupe_col_collection(self, obj, col_collection):
        dedupe = self.dedupe_columns
        if obj not in dedupe:
            dedupe.add(obj)
            col_collection.append(obj)

    @classmethod
    def _column_naming_convention(cls, label_style, legacy):

        if legacy:

            def name(col, col_name=None):
                if col_name:
                    return col_name
                else:
                    return getattr(col, "key")

            return name
        else:
            return SelectState._column_naming_convention(label_style)

    @classmethod
    def create_for_statement(cls, statement_container, compiler, **kw):
        """Create a context for a statement given a :class:`.Compiler`.

        This method is always invoked in the context of SQLCompiler.process().

        For a Select object, this would be invoked from
        SQLCompiler.visit_select(). For the special FromStatement object used
        by Query to indicate "Query.from_statement()", this is called by
        FromStatement._compiler_dispatch() that would be called by
        SQLCompiler.process().

        """
        raise NotImplementedError()

    @classmethod
    def get_column_descriptions(cls, statement):
        return _column_descriptions(statement)

    @classmethod
    def orm_pre_session_exec(
        cls,
        session,
        statement,
        params,
        execution_options,
        bind_arguments,
        is_reentrant_invoke,
    ):
        if is_reentrant_invoke:
            return statement, execution_options

        (
            load_options,
            execution_options,
        ) = QueryContext.default_load_options.from_execution_options(
            "_sa_orm_load_options",
            {"populate_existing", "autoflush", "yield_per"},
            execution_options,
            statement._execution_options,
        )

        # default execution options for ORM results:
        # 1. _result_disable_adapt_to_context=True
        #    this will disable the ResultSetMetadata._adapt_to_context()
        #    step which we don't need, as we have result processors cached
        #    against the original SELECT statement before caching.
        # 2. future_result=True.  The ORM should **never** resolve columns
        #    in a result set based on names, only on Column objects that
        #    are correctly adapted to the context.   W the legacy result
        #    it will still attempt name-based resolution and also emit a
        #    warning.
        if not execution_options:
            execution_options = _orm_load_exec_options
        else:
            execution_options = execution_options.union(_orm_load_exec_options)

        if load_options._yield_per:
            execution_options = execution_options.union(
                {"yield_per": load_options._yield_per}
            )

        bind_arguments["clause"] = statement

        # new in 1.4 - the coercions system is leveraged to allow the
        # "subject" mapper of a statement be propagated to the top
        # as the statement is built.   "subject" mapper is the generally
        # standard object used as an identifier for multi-database schemes.

        # we are here based on the fact that _propagate_attrs contains
        # "compile_state_plugin": "orm".   The "plugin_subject"
        # needs to be present as well.

        try:
            plugin_subject = statement._propagate_attrs["plugin_subject"]
        except KeyError:
            assert False, "statement had 'orm' plugin but no plugin_subject"
        else:
            if plugin_subject:
                bind_arguments["mapper"] = plugin_subject.mapper

        if load_options._autoflush:
            session._autoflush()

        return statement, execution_options

    @classmethod
    def orm_setup_cursor_result(
        cls,
        session,
        statement,
        params,
        execution_options,
        bind_arguments,
        result,
    ):
        execution_context = result.context
        compile_state = execution_context.compiled.compile_state

        # cover edge case where ORM entities used in legacy select
        # were passed to session.execute:
        # session.execute(legacy_select([User.id, User.name]))
        # see test_query->test_legacy_tuple_old_select

        load_options = execution_options.get(
            "_sa_orm_load_options", QueryContext.default_load_options
        )
        if compile_state.compile_options._is_star:
            return result

        querycontext = QueryContext(
            compile_state,
            statement,
            params,
            session,
            load_options,
            execution_options,
            bind_arguments,
        )
        return loading.instances(result, querycontext)

    @property
    def _lead_mapper_entities(self):
        """return all _MapperEntity objects in the lead entities collection.

        Does **not** include entities that have been replaced by
        with_entities(), with_only_columns()

        """
        return [
            ent for ent in self._entities if isinstance(ent, _MapperEntity)
        ]

    def _create_with_polymorphic_adapter(self, ext_info, selectable):
        """given MapperEntity or ORMColumnEntity, setup polymorphic loading
        if appropriate

        """
        if (
            not ext_info.is_aliased_class
            and ext_info.mapper.persist_selectable
            not in self._polymorphic_adapters
        ):
            for mp in ext_info.mapper.iterate_to_root():
                self._mapper_loads_polymorphically_with(
                    mp,
                    sql_util.ColumnAdapter(selectable, mp._equivalent_columns),
                )

    def _mapper_loads_polymorphically_with(self, mapper, adapter):
        for m2 in mapper._with_polymorphic_mappers or [mapper]:
            self._polymorphic_adapters[m2] = adapter
            for m in m2.iterate_to_root():  # TODO: redundant ?
                self._polymorphic_adapters[m.local_table] = adapter

    @classmethod
    def _create_entities_collection(cls, query, legacy):
        raise NotImplementedError(
            "this method only works for ORMSelectCompileState"
        )


@sql.base.CompileState.plugin_for("orm", "orm_from_statement")
class ORMFromStatementCompileState(ORMCompileState):
    _aliased_generations = util.immutabledict()
    _from_obj_alias = None
    _has_mapper_entities = False

    _has_orm_entities = False
    multi_row_eager_loaders = False
    eager_adding_joins = False
    compound_eager_adapter = None

    extra_criteria_entities = _EMPTY_DICT
    eager_joins = _EMPTY_DICT

    @classmethod
    def create_for_statement(cls, statement_container, compiler, **kw):

        if compiler is not None:
            toplevel = not compiler.stack
        else:
            toplevel = True

        self = cls.__new__(cls)
        self._primary_entity = None

        self.use_legacy_query_style = (
            statement_container._compile_options._use_legacy_query_style
        )
        self.statement_container = self.select_statement = statement_container
        self.requested_statement = statement = statement_container.element

        if statement.is_dml:
            self.dml_table = statement.table

        self._entities = []
        self._polymorphic_adapters = {}
        self._no_yield_pers = set()

        self.compile_options = statement_container._compile_options

        if (
            self.use_legacy_query_style
            and isinstance(statement, expression.SelectBase)
            and not statement._is_textual
            and not statement.is_dml
            and statement._label_style is LABEL_STYLE_NONE
        ):
            self.statement = statement.set_label_style(
                LABEL_STYLE_TABLENAME_PLUS_COL
            )
        else:
            self.statement = statement

        self._label_convention = self._column_naming_convention(
            statement._label_style
            if not statement._is_textual and not statement.is_dml
            else LABEL_STYLE_NONE,
            self.use_legacy_query_style,
        )

        _QueryEntity.to_compile_state(
            self,
            statement_container._raw_columns,
            self._entities,
            is_current_entities=True,
        )

        self.current_path = statement_container._compile_options._current_path

        if toplevel and statement_container._with_options:
            self.attributes = {"_unbound_load_dedupes": set()}
            self.global_attributes = compiler._global_attributes

            for opt in statement_container._with_options:
                if opt._is_compile_state:
                    opt.process_compile_state(self)

        else:
            self.attributes = {}
            self.global_attributes = compiler._global_attributes

        if statement_container._with_context_options:
            for fn, key in statement_container._with_context_options:
                fn(self)

        self.primary_columns = []
        self.secondary_columns = []
        self.dedupe_columns = set()
        self.create_eager_joins = []
        self._fallback_from_clauses = []

        self.order_by = None

        if isinstance(
            self.statement, (expression.TextClause, expression.UpdateBase)
        ):

            self.extra_criteria_entities = {}

            # setup for all entities. Currently, this is not useful
            # for eager loaders, as the eager loaders that work are able
            # to do their work entirely in row_processor.
            for entity in self._entities:
                entity.setup_compile_state(self)

            # we did the setup just to get primary columns.
            self.statement = _AdHocColumnsStatement(
                self.statement, self.primary_columns
            )
        else:
            # allow TextualSelect with implicit columns as well
            # as select() with ad-hoc columns, see test_query::TextTest
            self._from_obj_alias = sql.util.ColumnAdapter(
                self.statement, adapt_on_names=True
            )
            # set up for eager loaders, however if we fix subqueryload
            # it should not need to do this here.  the model of eager loaders
            # that can work entirely in row_processor might be interesting
            # here though subqueryloader has a lot of upfront work to do
            # see test/orm/test_query.py -> test_related_eagerload_against_text
            # for where this part makes a difference.  would rather have
            # subqueryload figure out what it needs more intelligently.
            #            for entity in self._entities:
            #                entity.setup_compile_state(self)

        return self

    def _adapt_col_list(self, cols, current_adapter):
        return cols

    def _get_current_adapter(self):
        return None


class _AdHocColumnsStatement(ClauseElement):
    """internal object created to somewhat act like a SELECT when we
    are selecting columns from a DML RETURNING.


    """

    __visit_name__ = None

    def __init__(self, text, columns):
        self.element = text
        self.column_args = [
            coercions.expect(roles.ColumnsClauseRole, c) for c in columns
        ]

    def _generate_cache_key(self):
        raise NotImplementedError()

    def _gen_cache_key(self, anon_map, bindparams):
        raise NotImplementedError()

    def _compiler_dispatch(
        self, compiler, compound_index=None, asfrom=False, **kw
    ):
        """provide a fixed _compiler_dispatch method."""

        toplevel = not compiler.stack
        entry = (
            compiler._default_stack_entry if toplevel else compiler.stack[-1]
        )

        populate_result_map = (
            toplevel
            # these two might not be needed
            or (
                compound_index == 0
                and entry.get("need_result_map_for_compound", False)
            )
            or entry.get("need_result_map_for_nested", False)
        )

        if populate_result_map:
            compiler._ordered_columns = (
                compiler._textual_ordered_columns
            ) = False

            # enable looser result column matching.  this is shown to be
            # needed by test_query.py::TextTest
            compiler._loose_column_name_matching = True

            for c in self.column_args:
                compiler.process(
                    c,
                    within_columns_clause=True,
                    add_to_result_map=compiler._add_to_result_map,
                )
        return compiler.process(self.element, **kw)


@sql.base.CompileState.plugin_for("orm", "select")
class ORMSelectCompileState(ORMCompileState, SelectState):
    _joinpath = _joinpoint = _EMPTY_DICT

    _memoized_entities = _EMPTY_DICT

    _from_obj_alias = None
    _has_mapper_entities = False

    _has_orm_entities = False
    multi_row_eager_loaders = False
    eager_adding_joins = False
    compound_eager_adapter = None

    correlate = None
    correlate_except = None
    _where_criteria = ()
    _having_criteria = ()

    @classmethod
    def create_for_statement(cls, statement, compiler, **kw):
        """compiler hook, we arrive here from compiler.visit_select() only."""

        self = cls.__new__(cls)

        if compiler is not None:
            toplevel = not compiler.stack
            self.global_attributes = compiler._global_attributes
        else:
            toplevel = True
            self.global_attributes = {}

        select_statement = statement

        # if we are a select() that was never a legacy Query, we won't
        # have ORM level compile options.
        statement._compile_options = cls.default_compile_options.safe_merge(
            statement._compile_options
        )

        if select_statement._execution_options:
            # execution options should not impact the compilation of a
            # query, and at the moment subqueryloader is putting some things
            # in here that we explicitly don't want stuck in a cache.
            self.select_statement = select_statement._clone()
            self.select_statement._execution_options = util.immutabledict()
        else:
            self.select_statement = select_statement

        # indicates this select() came from Query.statement
        self.for_statement = select_statement._compile_options._for_statement

        # generally if we are from Query or directly from a select()
        self.use_legacy_query_style = (
            select_statement._compile_options._use_legacy_query_style
        )

        self._entities = []
        self._primary_entity = None
        self._aliased_generations = {}
        self._polymorphic_adapters = {}
        self._no_yield_pers = set()

        # legacy: only for query.with_polymorphic()
        if select_statement._compile_options._with_polymorphic_adapt_map:
            self._with_polymorphic_adapt_map = dict(
                select_statement._compile_options._with_polymorphic_adapt_map
            )
            self._setup_with_polymorphics()

        self.compile_options = select_statement._compile_options

        if not toplevel:
            # for subqueries, turn off eagerloads and set
            # "render_for_subquery".
            self.compile_options += {
                "_enable_eagerloads": False,
                "_render_for_subquery": True,
            }

        # determine label style.   we can make different decisions here.
        # at the moment, trying to see if we can always use DISAMBIGUATE_ONLY
        # rather than LABEL_STYLE_NONE, and if we can use disambiguate style
        # for new style ORM selects too.
        if (
            self.use_legacy_query_style
            and self.select_statement._label_style is LABEL_STYLE_LEGACY_ORM
        ):
            if not self.for_statement:
                self.label_style = LABEL_STYLE_TABLENAME_PLUS_COL
            else:
                self.label_style = LABEL_STYLE_DISAMBIGUATE_ONLY
        else:
            self.label_style = self.select_statement._label_style

        if select_statement._memoized_select_entities:
            self._memoized_entities = {
                memoized_entities: _QueryEntity.to_compile_state(
                    self,
                    memoized_entities._raw_columns,
                    [],
                    is_current_entities=False,
                )
                for memoized_entities in (
                    select_statement._memoized_select_entities
                )
            }

        # label_convention is stateful and will yield deduping keys if it
        # sees the same key twice.  therefore it's important that it is not
        # invoked for the above "memoized" entities that aren't actually
        # in the columns clause
        self._label_convention = self._column_naming_convention(
            statement._label_style, self.use_legacy_query_style
        )

        _QueryEntity.to_compile_state(
            self,
            select_statement._raw_columns,
            self._entities,
            is_current_entities=True,
        )

        self.current_path = select_statement._compile_options._current_path

        self.eager_order_by = ()

        if toplevel and (
            select_statement._with_options
            or select_statement._memoized_select_entities
        ):
            self.attributes = {"_unbound_load_dedupes": set()}

            for (
                memoized_entities
            ) in select_statement._memoized_select_entities:
                for opt in memoized_entities._with_options:
                    if opt._is_compile_state:
                        opt.process_compile_state_replaced_entities(
                            self,
                            [
                                ent
                                for ent in self._memoized_entities[
                                    memoized_entities
                                ]
                                if isinstance(ent, _MapperEntity)
                            ],
                        )

            for opt in self.select_statement._with_options:
                if opt._is_compile_state:
                    opt.process_compile_state(self)
        else:
            self.attributes = {}

        if select_statement._with_context_options:
            for fn, key in select_statement._with_context_options:
                fn(self)

        self.primary_columns = []
        self.secondary_columns = []
        self.dedupe_columns = set()
        self.eager_joins = {}
        self.extra_criteria_entities = {}
        self.create_eager_joins = []
        self._fallback_from_clauses = []

        # normalize the FROM clauses early by themselves, as this makes
        # it an easier job when we need to assemble a JOIN onto these,
        # for select.join() as well as joinedload().   As of 1.4 there are now
        # potentially more complex sets of FROM objects here as the use
        # of lambda statements for lazyload, load_on_pk etc. uses more
        # cloning of the select() construct.  See #6495
        self.from_clauses = self._normalize_froms(
            info.selectable for info in select_statement._from_obj
        )

        # this is a fairly arbitrary break into a second method,
        # so it might be nicer to break up create_for_statement()
        # and _setup_for_generate into three or four logical sections
        self._setup_for_generate()

        SelectState.__init__(self, self.statement, compiler, **kw)

        return self

    def _setup_for_generate(self):
        query = self.select_statement

        self.statement = None
        self._join_entities = ()

        if self.compile_options._set_base_alias:
            self._set_select_from_alias()

        for memoized_entities in query._memoized_select_entities:
            if memoized_entities._setup_joins:
                self._join(
                    memoized_entities._setup_joins,
                    self._memoized_entities[memoized_entities],
                )
            if memoized_entities._legacy_setup_joins:
                self._legacy_join(
                    memoized_entities._legacy_setup_joins,
                    self._memoized_entities[memoized_entities],
                )

        if query._setup_joins:
            self._join(query._setup_joins, self._entities)

        if query._legacy_setup_joins:
            self._legacy_join(query._legacy_setup_joins, self._entities)

        current_adapter = self._get_current_adapter()

        if query._where_criteria:
            self._where_criteria = query._where_criteria

            if current_adapter:
                self._where_criteria = tuple(
                    current_adapter(crit, True)
                    for crit in self._where_criteria
                )

        # TODO: some complexity with order_by here was due to mapper.order_by.
        # now that this is removed we can hopefully make order_by /
        # group_by act identically to how they are in Core select.
        self.order_by = (
            self._adapt_col_list(query._order_by_clauses, current_adapter)
            if current_adapter and query._order_by_clauses not in (None, False)
            else query._order_by_clauses
        )

        if query._having_criteria:
            self._having_criteria = tuple(
                current_adapter(crit, True) if current_adapter else crit
                for crit in query._having_criteria
            )

        self.group_by = (
            self._adapt_col_list(
                util.flatten_iterator(query._group_by_clauses), current_adapter
            )
            if current_adapter and query._group_by_clauses not in (None, False)
            else query._group_by_clauses or None
        )

        if self.eager_order_by:
            adapter = self.from_clauses[0]._target_adapter
            self.eager_order_by = adapter.copy_and_process(self.eager_order_by)

        if query._distinct_on:
            self.distinct_on = self._adapt_col_list(
                query._distinct_on, current_adapter
            )
        else:
            self.distinct_on = ()

        self.distinct = query._distinct

        if query._correlate:
            # ORM mapped entities that are mapped to joins can be passed
            # to .correlate, so here they are broken into their component
            # tables.
            self.correlate = tuple(
                util.flatten_iterator(
                    sql_util.surface_selectables(s) if s is not None else None
                    for s in query._correlate
                )
            )
        elif query._correlate_except is not None:
            self.correlate_except = tuple(
                util.flatten_iterator(
                    sql_util.surface_selectables(s) if s is not None else None
                    for s in query._correlate_except
                )
            )
        elif not query._auto_correlate:
            self.correlate = (None,)

        # PART II

        self._for_update_arg = query._for_update_arg

        if self.compile_options._is_star and (len(self._entities) != 1):
            raise sa_exc.CompileError(
                "Can't generate ORM query that includes multiple expressions "
                "at the same time as '*'; query for '*' alone if present"
            )
        for entity in self._entities:
            entity.setup_compile_state(self)

        for rec in self.create_eager_joins:
            strategy = rec[0]
            strategy(self, *rec[1:])

        # else "load from discrete FROMs" mode,
        # i.e. when each _MappedEntity has its own FROM

        if self.compile_options._enable_single_crit:
            self._adjust_for_extra_criteria()

        if not self.primary_columns:
            if self.compile_options._only_load_props:
                raise sa_exc.InvalidRequestError(
                    "No column-based properties specified for "
                    "refresh operation. Use session.expire() "
                    "to reload collections and related items."
                )
            else:
                raise sa_exc.InvalidRequestError(
                    "Query contains no columns with which to SELECT from."
                )

        if not self.from_clauses:
            self.from_clauses = list(self._fallback_from_clauses)

        if self.order_by is False:
            self.order_by = None

        if (
            self.multi_row_eager_loaders
            and self.eager_adding_joins
            and self._should_nest_selectable
        ):
            self.statement = self._compound_eager_statement()
        else:
            self.statement = self._simple_statement()

        if self.for_statement:
            ezero = self._mapper_zero()
            if ezero is not None:
                # TODO: this goes away once we get rid of the deep entity
                # thing
                self.statement = self.statement._annotate(
                    {"deepentity": ezero}
                )

    @classmethod
    def _create_entities_collection(cls, query, legacy):
        """Creates a partial ORMSelectCompileState that includes
        the full collection of _MapperEntity and other _QueryEntity objects.

        Supports a few remaining use cases that are pre-compilation
        but still need to gather some of the column  / adaption information.

        """
        self = cls.__new__(cls)

        self._entities = []
        self._primary_entity = None
        self._aliased_generations = {}
        self._polymorphic_adapters = {}

        compile_options = cls.default_compile_options.safe_merge(
            query._compile_options
        )
        # legacy: only for query.with_polymorphic()
        if compile_options._with_polymorphic_adapt_map:
            self._with_polymorphic_adapt_map = dict(
                compile_options._with_polymorphic_adapt_map
            )
            self._setup_with_polymorphics()

        self._label_convention = self._column_naming_convention(
            query._label_style, legacy
        )

        # entities will also set up polymorphic adapters for mappers
        # that have with_polymorphic configured
        _QueryEntity.to_compile_state(
            self, query._raw_columns, self._entities, is_current_entities=True
        )
        return self

    @classmethod
    def determine_last_joined_entity(cls, statement):
        setup_joins = statement._setup_joins

        if not setup_joins:
            return None

        (target, onclause, from_, flags) = setup_joins[-1]

        if isinstance(target, interfaces.PropComparator):
            return target.entity
        else:
            return target

    @classmethod
    def all_selected_columns(cls, statement):
        for element in statement._raw_columns:
            if (
                element.is_selectable
                and "entity_namespace" in element._annotations
            ):
                ens = element._annotations["entity_namespace"]
                if not ens.is_mapper and not ens.is_aliased_class:
                    for elem in _select_iterables([element]):
                        yield elem
                else:
                    for elem in _select_iterables(ens._all_column_expressions):
                        yield elem
            else:
                for elem in _select_iterables([element]):
                    yield elem

    @classmethod
    def get_columns_clause_froms(cls, statement):
        return cls._normalize_froms(
            itertools.chain.from_iterable(
                element._from_objects
                if "parententity" not in element._annotations
                else [
                    element._annotations["parententity"].__clause_element__()
                ]
                for element in statement._raw_columns
            )
        )

    @classmethod
    @util.preload_module("sqlalchemy.orm.query")
    def from_statement(cls, statement, from_statement):
        query = util.preloaded.orm_query

        from_statement = coercions.expect(
            roles.ReturnsRowsRole,
            from_statement,
            apply_propagate_attrs=statement,
        )

        stmt = query.FromStatement(statement._raw_columns, from_statement)

        stmt.__dict__.update(
            _with_options=statement._with_options,
            _with_context_options=statement._with_context_options,
            _execution_options=statement._execution_options,
            _propagate_attrs=statement._propagate_attrs,
        )
        return stmt

    def _setup_with_polymorphics(self):
        # legacy: only for query.with_polymorphic()
        for ext_info, wp in self._with_polymorphic_adapt_map.items():
            self._mapper_loads_polymorphically_with(ext_info, wp._adapter)

    def _set_select_from_alias(self):

        query = self.select_statement  # query

        assert self.compile_options._set_base_alias
        assert len(query._from_obj) == 1

        adapter = self._get_select_from_alias_from_obj(query._from_obj[0])
        if adapter:
            self.compile_options += {"_enable_single_crit": False}
            self._from_obj_alias = adapter

    def _get_select_from_alias_from_obj(self, from_obj):
        info = from_obj

        if "parententity" in info._annotations:
            info = info._annotations["parententity"]

        if hasattr(info, "mapper"):
            if not info.is_aliased_class:
                raise sa_exc.ArgumentError(
                    "A selectable (FromClause) instance is "
                    "expected when the base alias is being set."
                )
            else:
                return info._adapter

        elif isinstance(info.selectable, sql.selectable.AliasedReturnsRows):
            equivs = self._all_equivs()
            return sql_util.ColumnAdapter(info, equivs)
        else:
            return None

    def _mapper_zero(self):
        """return the Mapper associated with the first QueryEntity."""
        return self._entities[0].mapper

    def _entity_zero(self):
        """Return the 'entity' (mapper or AliasedClass) associated
        with the first QueryEntity, or alternatively the 'select from'
        entity if specified."""

        for ent in self.from_clauses:
            if "parententity" in ent._annotations:
                return ent._annotations["parententity"]
        for qent in self._entities:
            if qent.entity_zero:
                return qent.entity_zero

        return None

    def _only_full_mapper_zero(self, methname):
        if self._entities != [self._primary_entity]:
            raise sa_exc.InvalidRequestError(
                "%s() can only be used against "
                "a single mapped class." % methname
            )
        return self._primary_entity.entity_zero

    def _only_entity_zero(self, rationale=None):
        if len(self._entities) > 1:
            raise sa_exc.InvalidRequestError(
                rationale
                or "This operation requires a Query "
                "against a single mapper."
            )
        return self._entity_zero()

    def _all_equivs(self):
        equivs = {}

        for memoized_entities in self._memoized_entities.values():
            for ent in [
                ent
                for ent in memoized_entities
                if isinstance(ent, _MapperEntity)
            ]:
                equivs.update(ent.mapper._equivalent_columns)

        for ent in [
            ent for ent in self._entities if isinstance(ent, _MapperEntity)
        ]:
            equivs.update(ent.mapper._equivalent_columns)
        return equivs

    def _compound_eager_statement(self):
        # for eager joins present and LIMIT/OFFSET/DISTINCT,
        # wrap the query inside a select,
        # then append eager joins onto that

        if self.order_by:
            # the default coercion for ORDER BY is now the OrderByRole,
            # which adds an additional post coercion to ByOfRole in that
            # elements are converted into label references.  For the
            # eager load / subquery wrapping case, we need to un-coerce
            # the original expressions outside of the label references
            # in order to have them render.
            unwrapped_order_by = [
                elem.element
                if isinstance(elem, sql.elements._label_reference)
                else elem
                for elem in self.order_by
            ]

            order_by_col_expr = sql_util.expand_column_list_from_order_by(
                self.primary_columns, unwrapped_order_by
            )
        else:
            order_by_col_expr = []
            unwrapped_order_by = None

        # put FOR UPDATE on the inner query, where MySQL will honor it,
        # as well as if it has an OF so PostgreSQL can use it.
        inner = self._select_statement(
            self.primary_columns
            + [c for c in order_by_col_expr if c not in self.dedupe_columns],
            self.from_clauses,
            self._where_criteria,
            self._having_criteria,
            self.label_style,
            self.order_by,
            for_update=self._for_update_arg,
            hints=self.select_statement._hints,
            statement_hints=self.select_statement._statement_hints,
            correlate=self.correlate,
            correlate_except=self.correlate_except,
            **self._select_args
        )

        inner = inner.alias()

        equivs = self._all_equivs()

        self.compound_eager_adapter = sql_util.ColumnAdapter(inner, equivs)

        statement = future.select(
            *([inner] + self.secondary_columns)  # use_labels=self.labels
        )
        statement._label_style = self.label_style

        # Oracle however does not allow FOR UPDATE on the subquery,
        # and the Oracle dialect ignores it, plus for PostgreSQL, MySQL
        # we expect that all elements of the row are locked, so also put it
        # on the outside (except in the case of PG when OF is used)
        if (
            self._for_update_arg is not None
            and self._for_update_arg.of is None
        ):
            statement._for_update_arg = self._for_update_arg

        from_clause = inner
        for eager_join in self.eager_joins.values():
            # EagerLoader places a 'stop_on' attribute on the join,
            # giving us a marker as to where the "splice point" of
            # the join should be
            from_clause = sql_util.splice_joins(
                from_clause, eager_join, eager_join.stop_on
            )

        statement.select_from.non_generative(statement, from_clause)

        if unwrapped_order_by:
            statement.order_by.non_generative(
                statement,
                *self.compound_eager_adapter.copy_and_process(
                    unwrapped_order_by
                )
            )

        statement.order_by.non_generative(statement, *self.eager_order_by)
        return statement

    def _simple_statement(self):

        if (
            self.compile_options._use_legacy_query_style
            and (self.distinct and not self.distinct_on)
            and self.order_by
        ):
            to_add = sql_util.expand_column_list_from_order_by(
                self.primary_columns, self.order_by
            )
            if to_add:
                util.warn_deprecated_20(
                    "ORDER BY columns added implicitly due to "
                    "DISTINCT is deprecated and will be removed in "
                    "SQLAlchemy 2.0.  SELECT statements with DISTINCT "
                    "should be written to explicitly include the appropriate "
                    "columns in the columns clause"
                )
            self.primary_columns += to_add

        statement = self._select_statement(
            self.primary_columns + self.secondary_columns,
            tuple(self.from_clauses) + tuple(self.eager_joins.values()),
            self._where_criteria,
            self._having_criteria,
            self.label_style,
            self.order_by,
            for_update=self._for_update_arg,
            hints=self.select_statement._hints,
            statement_hints=self.select_statement._statement_hints,
            correlate=self.correlate,
            correlate_except=self.correlate_except,
            **self._select_args
        )

        if self.eager_order_by:
            statement.order_by.non_generative(statement, *self.eager_order_by)
        return statement

    def _select_statement(
        self,
        raw_columns,
        from_obj,
        where_criteria,
        having_criteria,
        label_style,
        order_by,
        for_update,
        hints,
        statement_hints,
        correlate,
        correlate_except,
        limit_clause,
        offset_clause,
        fetch_clause,
        fetch_clause_options,
        distinct,
        distinct_on,
        prefixes,
        suffixes,
        group_by,
    ):

        Select = future.Select
        statement = Select._create_raw_select(
            _raw_columns=raw_columns,
            _from_obj=from_obj,
            _label_style=label_style,
        )

        if where_criteria:
            statement._where_criteria = where_criteria
        if having_criteria:
            statement._having_criteria = having_criteria

        if order_by:
            statement._order_by_clauses += tuple(order_by)

        if distinct_on:
            statement.distinct.non_generative(statement, *distinct_on)
        elif distinct:
            statement.distinct.non_generative(statement)

        if group_by:
            statement._group_by_clauses += tuple(group_by)

        statement._limit_clause = limit_clause
        statement._offset_clause = offset_clause
        statement._fetch_clause = fetch_clause
        statement._fetch_clause_options = fetch_clause_options

        if prefixes:
            statement._prefixes = prefixes

        if suffixes:
            statement._suffixes = suffixes

        statement._for_update_arg = for_update

        if hints:
            statement._hints = hints
        if statement_hints:
            statement._statement_hints = statement_hints

        if correlate:
            statement.correlate.non_generative(statement, *correlate)

        if correlate_except is not None:
            statement.correlate_except.non_generative(
                statement, *correlate_except
            )

        return statement

    def _adapt_polymorphic_element(self, element):
        if "parententity" in element._annotations:
            search = element._annotations["parententity"]
            alias = self._polymorphic_adapters.get(search, None)
            if alias:
                return alias.adapt_clause(element)

        if isinstance(element, expression.FromClause):
            search = element
        elif hasattr(element, "table"):
            search = element.table
        else:
            return None

        alias = self._polymorphic_adapters.get(search, None)
        if alias:
            return alias.adapt_clause(element)

    def _adapt_aliased_generation(self, element):
        # this is crazy logic that I look forward to blowing away
        # when aliased=True is gone :)
        if "aliased_generation" in element._annotations:
            for adapter in self._aliased_generations.get(
                element._annotations["aliased_generation"], ()
            ):
                replaced_elem = adapter.replace(element)
                if replaced_elem is not None:
                    return replaced_elem

        return None

    def _adapt_col_list(self, cols, current_adapter):
        if current_adapter:
            return [current_adapter(o, True) for o in cols]
        else:
            return cols

    def _get_current_adapter(self):

        adapters = []

        if self._from_obj_alias:
            # used for legacy going forward for query set_ops, e.g.
            # union(), union_all(), etc.
            # 1.4 and previously, also used for from_self(),
            # select_entity_from()
            #
            # for the "from obj" alias, apply extra rule to the
            # 'ORM only' check, if this query were generated from a
            # subquery of itself, i.e. _from_selectable(), apply adaption
            # to all SQL constructs.
            adapters.append(
                (
                    False
                    if self.compile_options._orm_only_from_obj_alias
                    else True,
                    self._from_obj_alias.replace,
                )
            )

        # vvvvvvvvvvvvvvv legacy vvvvvvvvvvvvvvvvvv
        # this can totally go away when we remove join(..., aliased=True)
        if self._aliased_generations:
            adapters.append((False, self._adapt_aliased_generation))
        # ^^^^^^^^^^^^^ legacy ^^^^^^^^^^^^^^^^^^^^^

        # this was *hopefully* the only adapter we were going to need
        # going forward...however, we unfortunately need _from_obj_alias
        # for query.union(), which we can't drop
        if self._polymorphic_adapters:
            adapters.append((False, self._adapt_polymorphic_element))

        if not adapters:
            return None

        def _adapt_clause(clause, as_filter):
            # do we adapt all expression elements or only those
            # tagged as 'ORM' constructs ?

            def replace(elem):
                is_orm_adapt = (
                    "_orm_adapt" in elem._annotations
                    or "parententity" in elem._annotations
                )
                for always_adapt, adapter in adapters:
                    if is_orm_adapt or always_adapt:
                        e = adapter(elem)
                        if e is not None:
                            return e

            return visitors.replacement_traverse(clause, {}, replace)

        return _adapt_clause

    def _join(self, args, entities_collection):
        for (right, onclause, from_, flags) in args:
            isouter = flags["isouter"]
            full = flags["full"]
            # maybe?
            self._reset_joinpoint()

            right = inspect(right)
            if onclause is not None:
                onclause = inspect(onclause)

            if onclause is None and isinstance(
                right, interfaces.PropComparator
            ):
                # determine onclause/right_entity.  still need to think
                # about how to best organize this since we are getting:
                #
                #
                # q.join(Entity, Parent.property)
                # q.join(Parent.property)
                # q.join(Parent.property.of_type(Entity))
                # q.join(some_table)
                # q.join(some_table, some_parent.c.id==some_table.c.parent_id)
                #
                # is this still too many choices?  how do we handle this
                # when sometimes "right" is implied and sometimes not?
                #
                onclause = right
                right = None
            elif "parententity" in right._annotations:
                right = right._annotations["parententity"]

            if onclause is None:
                if not right.is_selectable and not hasattr(right, "mapper"):
                    raise sa_exc.ArgumentError(
                        "Expected mapped entity or "
                        "selectable/table as join target"
                    )

            of_type = None

            if isinstance(onclause, interfaces.PropComparator):
                # descriptor/property given (or determined); this tells us
                # explicitly what the expected "left" side of the join is.

                of_type = getattr(onclause, "_of_type", None)

                if right is None:
                    if of_type:
                        right = of_type
                    else:
                        right = onclause.property

                        try:
                            right = right.entity
                        except AttributeError as err:
                            util.raise_(
                                sa_exc.ArgumentError(
                                    "Join target %s does not refer to a "
                                    "mapped entity" % right
                                ),
                                replace_context=err,
                            )

                left = onclause._parententity

                alias = self._polymorphic_adapters.get(left, None)

                # could be None or could be ColumnAdapter also
                if isinstance(alias, ORMAdapter) and alias.mapper.isa(left):
                    left = alias.aliased_class
                    onclause = getattr(left, onclause.key)

                prop = onclause.property
                if not isinstance(onclause, attributes.QueryableAttribute):
                    onclause = prop

                # TODO: this is where "check for path already present"
                # would occur. see if this still applies?

                if from_ is not None:
                    if (
                        from_ is not left
                        and from_._annotations.get("parententity", None)
                        is not left
                    ):
                        raise sa_exc.InvalidRequestError(
                            "explicit from clause %s does not match left side "
                            "of relationship attribute %s"
                            % (
                                from_._annotations.get("parententity", from_),
                                onclause,
                            )
                        )
            elif from_ is not None:
                prop = None
                left = from_
            else:
                # no descriptor/property given; we will need to figure out
                # what the effective "left" side is
                prop = left = None

            # figure out the final "left" and "right" sides and create an
            # ORMJoin to add to our _from_obj tuple
            self._join_left_to_right(
                entities_collection,
                left,
                right,
                onclause,
                prop,
                False,
                False,
                isouter,
                full,
            )

    def _legacy_join(self, args, entities_collection):
        """consumes arguments from join() or outerjoin(), places them into a
        consistent format with which to form the actual JOIN constructs.

        """
        for (right, onclause, left, flags) in args:

            outerjoin = flags["isouter"]
            create_aliases = flags["aliased"]
            from_joinpoint = flags["from_joinpoint"]
            full = flags["full"]
            aliased_generation = flags["aliased_generation"]

            # do a quick inspect to accommodate for a lambda
            if right is not None and not isinstance(right, util.string_types):
                right = inspect(right)
            if onclause is not None and not isinstance(
                onclause, util.string_types
            ):
                onclause = inspect(onclause)

            # legacy vvvvvvvvvvvvvvvvvvvvvvvvvv
            if not from_joinpoint:
                self._reset_joinpoint()
            else:
                prev_aliased_generation = self._joinpoint.get(
                    "aliased_generation", None
                )
                if not aliased_generation:
                    aliased_generation = prev_aliased_generation
                elif prev_aliased_generation:
                    self._aliased_generations[
                        aliased_generation
                    ] = self._aliased_generations.get(
                        prev_aliased_generation, ()
                    )
            # legacy ^^^^^^^^^^^^^^^^^^^^^^^^^^^

            if (
                isinstance(
                    right, (interfaces.PropComparator, util.string_types)
                )
                and onclause is None
            ):
                onclause = right
                right = None
            elif "parententity" in right._annotations:
                right = right._annotations["parententity"]

            if onclause is None:
                if not right.is_selectable and not hasattr(right, "mapper"):
                    raise sa_exc.ArgumentError(
                        "Expected mapped entity or "
                        "selectable/table as join target"
                    )

            if isinstance(onclause, interfaces.PropComparator):
                of_type = getattr(onclause, "_of_type", None)
            else:
                of_type = None

            if isinstance(onclause, util.string_types):
                # string given, e.g. query(Foo).join("bar").
                # we look to the left entity or what we last joined
                # towards
                onclause = _entity_namespace_key(
                    inspect(self._joinpoint_zero()), onclause
                )

            # legacy vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
            # check for q.join(Class.propname, from_joinpoint=True)
            # and Class corresponds at the mapper level to the current
            # joinpoint.  this match intentionally looks for a non-aliased
            # class-bound descriptor as the onclause and if it matches the
            # current joinpoint at the mapper level, it's used.  This
            # is a very old use case that is intended to make it easier
            # to work with the aliased=True flag, which is also something
            # that probably shouldn't exist on join() due to its high
            # complexity/usefulness ratio
            elif from_joinpoint and isinstance(
                onclause, interfaces.PropComparator
            ):
                jp0 = self._joinpoint_zero()
                info = inspect(jp0)

                if getattr(info, "mapper", None) is onclause._parententity:
                    onclause = _entity_namespace_key(info, onclause.key)
            # legacy ^^^^^^^^^^^^^^^^^^^^^^^^^^^

            if isinstance(onclause, interfaces.PropComparator):
                # descriptor/property given (or determined); this tells us
                # explicitly what the expected "left" side of the join is.
                if right is None:
                    if of_type:
                        right = of_type
                    else:
                        right = onclause.property

                        try:
                            right = right.entity
                        except AttributeError as err:
                            util.raise_(
                                sa_exc.ArgumentError(
                                    "Join target %s does not refer to a "
                                    "mapped entity" % right
                                ),
                                replace_context=err,
                            )

                left = onclause._parententity

                alias = self._polymorphic_adapters.get(left, None)

                # could be None or could be ColumnAdapter also
                if isinstance(alias, ORMAdapter) and alias.mapper.isa(left):
                    left = alias.aliased_class
                    onclause = getattr(left, onclause.key)

                prop = onclause.property
                if not isinstance(onclause, attributes.QueryableAttribute):
                    onclause = prop

                if not create_aliases:
                    # check for this path already present.
                    # don't render in that case.
                    edge = (left, right, prop.key)
                    if edge in self._joinpoint:
                        # The child's prev reference might be stale --
                        # it could point to a parent older than the
                        # current joinpoint.  If this is the case,
                        # then we need to update it and then fix the
                        # tree's spine with _update_joinpoint.  Copy
                        # and then mutate the child, which might be
                        # shared by a different query object.
                        jp = self._joinpoint[edge].copy()
                        jp["prev"] = (edge, self._joinpoint)
                        self._update_joinpoint(jp)

                        continue

            else:
                # no descriptor/property given; we will need to figure out
                # what the effective "left" side is
                prop = left = None

            # figure out the final "left" and "right" sides and create an
            # ORMJoin to add to our _from_obj tuple
            self._join_left_to_right(
                entities_collection,
                left,
                right,
                onclause,
                prop,
                create_aliases,
                aliased_generation,
                outerjoin,
                full,
            )

    def _joinpoint_zero(self):
        return self._joinpoint.get("_joinpoint_entity", self._entity_zero())

    def _join_left_to_right(
        self,
        entities_collection,
        left,
        right,
        onclause,
        prop,
        create_aliases,
        aliased_generation,
        outerjoin,
        full,
    ):
        """given raw "left", "right", "onclause" parameters consumed from
        a particular key within _join(), add a real ORMJoin object to
        our _from_obj list (or augment an existing one)

        """

        if left is None:
            # left not given (e.g. no relationship object/name specified)
            # figure out the best "left" side based on our existing froms /
            # entities
            assert prop is None
            (
                left,
                replace_from_obj_index,
                use_entity_index,
            ) = self._join_determine_implicit_left_side(
                entities_collection, left, right, onclause
            )
        else:
            # left is given via a relationship/name, or as explicit left side.
            # Determine where in our
            # "froms" list it should be spliced/appended as well as what
            # existing entity it corresponds to.
            (
                replace_from_obj_index,
                use_entity_index,
            ) = self._join_place_explicit_left_side(entities_collection, left)

        if left is right and not create_aliases:
            raise sa_exc.InvalidRequestError(
                "Can't construct a join from %s to %s, they "
                "are the same entity" % (left, right)
            )

        # the right side as given often needs to be adapted.  additionally
        # a lot of things can be wrong with it.  handle all that and
        # get back the new effective "right" side
        r_info, right, onclause = self._join_check_and_adapt_right_side(
            left, right, onclause, prop, create_aliases, aliased_generation
        )

        if not r_info.is_selectable:
            extra_criteria = self._get_extra_criteria(r_info)
        else:
            extra_criteria = ()

        if replace_from_obj_index is not None:
            # splice into an existing element in the
            # self._from_obj list
            left_clause = self.from_clauses[replace_from_obj_index]

            self.from_clauses = (
                self.from_clauses[:replace_from_obj_index]
                + [
                    _ORMJoin(
                        left_clause,
                        right,
                        onclause,
                        isouter=outerjoin,
                        full=full,
                        _extra_criteria=extra_criteria,
                    )
                ]
                + self.from_clauses[replace_from_obj_index + 1 :]
            )
        else:
            # add a new element to the self._from_obj list
            if use_entity_index is not None:
                # make use of _MapperEntity selectable, which is usually
                # entity_zero.selectable, but if with_polymorphic() were used
                # might be distinct
                assert isinstance(
                    entities_collection[use_entity_index], _MapperEntity
                )
                left_clause = entities_collection[use_entity_index].selectable
            else:
                left_clause = left

            self.from_clauses = self.from_clauses + [
                _ORMJoin(
                    left_clause,
                    r_info,
                    onclause,
                    isouter=outerjoin,
                    full=full,
                    _extra_criteria=extra_criteria,
                )
            ]

    def _join_determine_implicit_left_side(
        self, entities_collection, left, right, onclause
    ):
        """When join conditions don't express the left side explicitly,
        determine if an existing FROM or entity in this query
        can serve as the left hand side.

        """

        # when we are here, it means join() was called without an ORM-
        # specific way of telling us what the "left" side is, e.g.:
        #
        # join(RightEntity)
        #
        # or
        #
        # join(RightEntity, RightEntity.foo == LeftEntity.bar)
        #

        r_info = inspect(right)

        replace_from_obj_index = use_entity_index = None

        if self.from_clauses:
            # we have a list of FROMs already.  So by definition this
            # join has to connect to one of those FROMs.

            indexes = sql_util.find_left_clause_to_join_from(
                self.from_clauses, r_info.selectable, onclause
            )

            if len(indexes) == 1:
                replace_from_obj_index = indexes[0]
                left = self.from_clauses[replace_from_obj_index]
            elif len(indexes) > 1:
                raise sa_exc.InvalidRequestError(
                    "Can't determine which FROM clause to join "
                    "from, there are multiple FROMS which can "
                    "join to this entity. Please use the .select_from() "
                    "method to establish an explicit left side, as well as "
                    "providing an explicit ON clause if not present already "
                    "to help resolve the ambiguity."
                )
            else:
                raise sa_exc.InvalidRequestError(
                    "Don't know how to join to %r. "
                    "Please use the .select_from() "
                    "method to establish an explicit left side, as well as "
                    "providing an explicit ON clause if not present already "
                    "to help resolve the ambiguity." % (right,)
                )

        elif entities_collection:
            # we have no explicit FROMs, so the implicit left has to
            # come from our list of entities.

            potential = {}
            for entity_index, ent in enumerate(entities_collection):
                entity = ent.entity_zero_or_selectable
                if entity is None:
                    continue
                ent_info = inspect(entity)
                if ent_info is r_info:  # left and right are the same, skip
                    continue

                # by using a dictionary with the selectables as keys this
                # de-duplicates those selectables as occurs when the query is
                # against a series of columns from the same selectable
                if isinstance(ent, _MapperEntity):
                    potential[ent.selectable] = (entity_index, entity)
                else:
                    potential[ent_info.selectable] = (None, entity)

            all_clauses = list(potential.keys())
            indexes = sql_util.find_left_clause_to_join_from(
                all_clauses, r_info.selectable, onclause
            )

            if len(indexes) == 1:
                use_entity_index, left = potential[all_clauses[indexes[0]]]
            elif len(indexes) > 1:
                raise sa_exc.InvalidRequestError(
                    "Can't determine which FROM clause to join "
                    "from, there are multiple FROMS which can "
                    "join to this entity. Please use the .select_from() "
                    "method to establish an explicit left side, as well as "
                    "providing an explicit ON clause if not present already "
                    "to help resolve the ambiguity."
                )
            else:
                raise sa_exc.InvalidRequestError(
                    "Don't know how to join to %r. "
                    "Please use the .select_from() "
                    "method to establish an explicit left side, as well as "
                    "providing an explicit ON clause if not present already "
                    "to help resolve the ambiguity." % (right,)
                )
        else:
            raise sa_exc.InvalidRequestError(
                "No entities to join from; please use "
                "select_from() to establish the left "
                "entity/selectable of this join"
            )

        return left, replace_from_obj_index, use_entity_index

    def _join_place_explicit_left_side(self, entities_collection, left):
        """When join conditions express a left side explicitly, determine
        where in our existing list of FROM clauses we should join towards,
        or if we need to make a new join, and if so is it from one of our
        existing entities.

        """

        # when we are here, it means join() was called with an indicator
        # as to an exact left side, which means a path to a
        # RelationshipProperty was given, e.g.:
        #
        # join(RightEntity, LeftEntity.right)
        #
        # or
        #
        # join(LeftEntity.right)
        #
        # as well as string forms:
        #
        # join(RightEntity, "right")
        #
        # etc.
        #

        replace_from_obj_index = use_entity_index = None

        l_info = inspect(left)
        if self.from_clauses:
            indexes = sql_util.find_left_clause_that_matches_given(
                self.from_clauses, l_info.selectable
            )

            if len(indexes) > 1:
                raise sa_exc.InvalidRequestError(
                    "Can't identify which entity in which to assign the "
                    "left side of this join.   Please use a more specific "
                    "ON clause."
                )

            # have an index, means the left side is already present in
            # an existing FROM in the self._from_obj tuple
            if indexes:
                replace_from_obj_index = indexes[0]

            # no index, means we need to add a new element to the
            # self._from_obj tuple

        # no from element present, so we will have to add to the
        # self._from_obj tuple.  Determine if this left side matches up
        # with existing mapper entities, in which case we want to apply the
        # aliasing / adaptation rules present on that entity if any
        if (
            replace_from_obj_index is None
            and entities_collection
            and hasattr(l_info, "mapper")
        ):
            for idx, ent in enumerate(entities_collection):
                # TODO: should we be checking for multiple mapper entities
                # matching?
                if isinstance(ent, _MapperEntity) and ent.corresponds_to(left):
                    use_entity_index = idx
                    break

        return replace_from_obj_index, use_entity_index

    def _join_check_and_adapt_right_side(
        self, left, right, onclause, prop, create_aliases, aliased_generation
    ):
        """transform the "right" side of the join as well as the onclause
        according to polymorphic mapping translations, aliasing on the query
        or on the join, special cases where the right and left side have
        overlapping tables.

        """

        l_info = inspect(left)
        r_info = inspect(right)

        overlap = False
        if not create_aliases:
            right_mapper = getattr(r_info, "mapper", None)
            # if the target is a joined inheritance mapping,
            # be more liberal about auto-aliasing.
            if right_mapper and (
                right_mapper.with_polymorphic
                or isinstance(right_mapper.persist_selectable, expression.Join)
            ):
                for from_obj in self.from_clauses or [l_info.selectable]:
                    if sql_util.selectables_overlap(
                        l_info.selectable, from_obj
                    ) and sql_util.selectables_overlap(
                        from_obj, r_info.selectable
                    ):
                        overlap = True
                        break

        if (
            overlap or not create_aliases
        ) and l_info.selectable is r_info.selectable:
            raise sa_exc.InvalidRequestError(
                "Can't join table/selectable '%s' to itself"
                % l_info.selectable
            )

        right_mapper, right_selectable, right_is_aliased = (
            getattr(r_info, "mapper", None),
            r_info.selectable,
            getattr(r_info, "is_aliased_class", False),
        )

        if (
            right_mapper
            and prop
            and not right_mapper.common_parent(prop.mapper)
        ):
            raise sa_exc.InvalidRequestError(
                "Join target %s does not correspond to "
                "the right side of join condition %s" % (right, onclause)
            )

        # _join_entities is used as a hint for single-table inheritance
        # purposes at the moment
        if hasattr(r_info, "mapper"):
            self._join_entities += (r_info,)

        need_adapter = False

        # test for joining to an unmapped selectable as the target
        if r_info.is_clause_element:

            if prop:
                right_mapper = prop.mapper

            if right_selectable._is_lateral:
                # orm_only is disabled to suit the case where we have to
                # adapt an explicit correlate(Entity) - the select() loses
                # the ORM-ness in this case right now, ideally it would not
                current_adapter = self._get_current_adapter()
                if current_adapter is not None:
                    # TODO: we had orm_only=False here before, removing
                    # it didn't break things.   if we identify the rationale,
                    # may need to apply "_orm_only" annotation here.
                    right = current_adapter(right, True)

            elif prop:
                # joining to selectable with a mapper property given
                # as the ON clause

                if not right_selectable.is_derived_from(
                    right_mapper.persist_selectable
                ):
                    raise sa_exc.InvalidRequestError(
                        "Selectable '%s' is not derived from '%s'"
                        % (
                            right_selectable.description,
                            right_mapper.persist_selectable.description,
                        )
                    )

                # if the destination selectable is a plain select(),
                # turn it into an alias().
                if isinstance(right_selectable, expression.SelectBase):
                    right_selectable = coercions.expect(
                        roles.FromClauseRole, right_selectable
                    )
                    need_adapter = True

                # make the right hand side target into an ORM entity
                right = aliased(right_mapper, right_selectable)

                util.warn_deprecated(
                    "An alias is being generated automatically against "
                    "joined entity %s for raw clauseelement, which is "
                    "deprecated and will be removed in a later release. "
                    "Use the aliased() "
                    "construct explicitly, see the linked example."
                    % right_mapper,
                    "1.4",
                    code="xaj1",
                )

            elif create_aliases:
                # it *could* work, but it doesn't right now and I'd rather
                # get rid of aliased=True completely
                raise sa_exc.InvalidRequestError(
                    "The aliased=True parameter on query.join() only works "
                    "with an ORM entity, not a plain selectable, as the "
                    "target."
                )

        # test for overlap:
        # orm/inheritance/relationships.py
        # SelfReferentialM2MTest
        aliased_entity = right_mapper and not right_is_aliased and overlap

        if not need_adapter and (create_aliases or aliased_entity):
            # there are a few places in the ORM that automatic aliasing
            # is still desirable, and can't be automatic with a Core
            # only approach.  For illustrations of "overlaps" see
            # test/orm/inheritance/test_relationships.py.  There are also
            # general overlap cases with many-to-many tables where automatic
            # aliasing is desirable.
            right = aliased(right, flat=True)
            need_adapter = True

            if not create_aliases:
                util.warn(
                    "An alias is being generated automatically against "
                    "joined entity %s due to overlapping tables.  This is a "
                    "legacy pattern which may be "
                    "deprecated in a later release.  Use the "
                    "aliased(<entity>, flat=True) "
                    "construct explicitly, see the linked example."
                    % right_mapper,
                    code="xaj2",
                )

        if need_adapter:
            assert right_mapper

            adapter = ORMAdapter(
                right, equivalents=right_mapper._equivalent_columns
            )

            # if an alias() on the right side was generated,
            # which is intended to wrap a the right side in a subquery,
            # ensure that columns retrieved from this target in the result
            # set are also adapted.
            if not create_aliases:
                self._mapper_loads_polymorphically_with(right_mapper, adapter)
            elif aliased_generation:
                adapter._debug = True
                self._aliased_generations[aliased_generation] = (
                    adapter,
                ) + self._aliased_generations.get(aliased_generation, ())
        elif (
            not r_info.is_clause_element
            and not right_is_aliased
            and right_mapper.with_polymorphic
            and isinstance(
                right_mapper._with_polymorphic_selectable,
                expression.AliasedReturnsRows,
            )
        ):
            # for the case where the target mapper has a with_polymorphic
            # set up, ensure an adapter is set up for criteria that works
            # against this mapper.  Previously, this logic used to
            # use the "create_aliases or aliased_entity" case to generate
            # an aliased() object, but this creates an alias that isn't
            # strictly necessary.
            # see test/orm/test_core_compilation.py
            # ::RelNaturalAliasedJoinsTest::test_straight
            # and similar
            self._mapper_loads_polymorphically_with(
                right_mapper,
                sql_util.ColumnAdapter(
                    right_mapper.selectable,
                    right_mapper._equivalent_columns,
                ),
            )
        # if the onclause is a ClauseElement, adapt it with any
        # adapters that are in place right now
        if isinstance(onclause, expression.ClauseElement):
            current_adapter = self._get_current_adapter()
            if current_adapter:
                onclause = current_adapter(onclause, True)

        # if joining on a MapperProperty path,
        # track the path to prevent redundant joins
        if not create_aliases and prop:
            self._update_joinpoint(
                {
                    "_joinpoint_entity": right,
                    "prev": ((left, right, prop.key), self._joinpoint),
                    "aliased_generation": aliased_generation,
                }
            )
        else:
            self._joinpoint = {
                "_joinpoint_entity": right,
                "aliased_generation": aliased_generation,
            }

        return inspect(right), right, onclause

    def _update_joinpoint(self, jp):
        self._joinpoint = jp
        # copy backwards to the root of the _joinpath
        # dict, so that no existing dict in the path is mutated
        while "prev" in jp:
            f, prev = jp["prev"]
            prev = dict(prev)
            prev[f] = jp.copy()
            jp["prev"] = (f, prev)
            jp = prev
        self._joinpath = jp

    def _reset_joinpoint(self):
        self._joinpoint = self._joinpath

    @property
    def _select_args(self):
        return {
            "limit_clause": self.select_statement._limit_clause,
            "offset_clause": self.select_statement._offset_clause,
            "distinct": self.distinct,
            "distinct_on": self.distinct_on,
            "prefixes": self.select_statement._prefixes,
            "suffixes": self.select_statement._suffixes,
            "group_by": self.group_by or None,
            "fetch_clause": self.select_statement._fetch_clause,
            "fetch_clause_options": (
                self.select_statement._fetch_clause_options
            ),
        }

    @property
    def _should_nest_selectable(self):
        kwargs = self._select_args
        return (
            kwargs.get("limit_clause") is not None
            or kwargs.get("offset_clause") is not None
            or kwargs.get("distinct", False)
            or kwargs.get("distinct_on", ())
            or kwargs.get("group_by", False)
        )

    def _get_extra_criteria(self, ext_info):
        if (
            "additional_entity_criteria",
            ext_info.mapper,
        ) in self.global_attributes:
            return tuple(
                ae._resolve_where_criteria(ext_info)
                for ae in self.global_attributes[
                    ("additional_entity_criteria", ext_info.mapper)
                ]
                if (ae.include_aliases or ae.entity is ext_info)
                and ae._should_include(self)
            )
        else:
            return ()

    def _adjust_for_extra_criteria(self):
        """Apply extra criteria filtering.

        For all distinct single-table-inheritance mappers represented in
        the columns clause of this query, as well as the "select from entity",
        add criterion to the WHERE
        clause of the given QueryContext such that only the appropriate
        subtypes are selected from the total results.

        Additionally, add WHERE criteria originating from LoaderCriteriaOptions
        associated with the global context.

        """

        for fromclause in self.from_clauses:
            ext_info = fromclause._annotations.get("parententity", None)

            if (
                ext_info
                and (
                    ext_info.mapper._single_table_criterion is not None
                    or ("additional_entity_criteria", ext_info.mapper)
                    in self.global_attributes
                )
                and ext_info not in self.extra_criteria_entities
            ):

                self.extra_criteria_entities[ext_info] = (
                    ext_info,
                    ext_info._adapter if ext_info.is_aliased_class else None,
                )

        search = set(self.extra_criteria_entities.values())

        for (ext_info, adapter) in search:
            if ext_info in self._join_entities:
                continue

            single_crit = ext_info.mapper._single_table_criterion

            if self.compile_options._for_refresh_state:
                additional_entity_criteria = []
            else:
                additional_entity_criteria = self._get_extra_criteria(ext_info)

            if single_crit is not None:
                additional_entity_criteria += (single_crit,)

            current_adapter = self._get_current_adapter()
            for crit in additional_entity_criteria:
                if adapter:
                    crit = adapter.traverse(crit)

                if current_adapter:
                    crit = sql_util._deep_annotate(crit, {"_orm_adapt": True})
                    crit = current_adapter(crit, False)
                self._where_criteria += (crit,)


def _column_descriptions(
    query_or_select_stmt, compile_state=None, legacy=False
):
    if compile_state is None:
        compile_state = ORMSelectCompileState._create_entities_collection(
            query_or_select_stmt, legacy=legacy
        )
    ctx = compile_state
    return [
        {
            "name": ent._label_name,
            "type": ent.type,
            "aliased": getattr(insp_ent, "is_aliased_class", False),
            "expr": ent.expr,
            "entity": getattr(insp_ent, "entity", None)
            if ent.entity_zero is not None and not insp_ent.is_clause_element
            else None,
        }
        for ent, insp_ent in [
            (
                _ent,
                (
                    inspect(_ent.entity_zero)
                    if _ent.entity_zero is not None
                    else None
                ),
            )
            for _ent in ctx._entities
        ]
    ]


def _legacy_filter_by_entity_zero(query_or_augmented_select):
    self = query_or_augmented_select
    if self._legacy_setup_joins:
        _last_joined_entity = self._last_joined_entity
        if _last_joined_entity is not None:
            return _last_joined_entity

    if self._from_obj and "parententity" in self._from_obj[0]._annotations:
        return self._from_obj[0]._annotations["parententity"]

    return _entity_from_pre_ent_zero(self)


def _entity_from_pre_ent_zero(query_or_augmented_select):
    self = query_or_augmented_select
    if not self._raw_columns:
        return None

    ent = self._raw_columns[0]

    if "parententity" in ent._annotations:
        return ent._annotations["parententity"]
    elif isinstance(ent, ORMColumnsClauseRole):
        return ent.entity
    elif "bundle" in ent._annotations:
        return ent._annotations["bundle"]
    else:
        return ent


def _legacy_determine_last_joined_entity(setup_joins, entity_zero):
    """given the legacy_setup_joins collection at a point in time,
    figure out what the "filter by entity" would be in terms
    of those joins.

    in 2.0 this logic should hopefully be much simpler as there will
    be far fewer ways to specify joins with the ORM

    """

    if not setup_joins:
        return entity_zero

    # CAN BE REMOVED IN 2.0:
    # 1. from_joinpoint
    # 2. aliased_generation
    # 3. aliased
    # 4. any treating of prop as str
    # 5. tuple madness
    # 6. won't need recursive call anymore without #4
    # 7. therefore can pass in just the last setup_joins record,
    #    don't need entity_zero

    (right, onclause, left_, flags) = setup_joins[-1]

    from_joinpoint = flags["from_joinpoint"]

    if onclause is None and isinstance(
        right, (str, interfaces.PropComparator)
    ):
        onclause = right
        right = None

    if right is not None and "parententity" in right._annotations:
        right = right._annotations["parententity"].entity

    if right is not None:
        last_entity = right
        insp = inspect(last_entity)
        if insp.is_clause_element or insp.is_aliased_class or insp.is_mapper:
            return insp

    last_entity = onclause
    if isinstance(last_entity, interfaces.PropComparator):
        return last_entity.entity

    # legacy vvvvvvvvvvvvvvvvvvvvvvvvvvv
    if isinstance(onclause, str):
        if from_joinpoint:
            prev = _legacy_determine_last_joined_entity(
                setup_joins[0:-1], entity_zero
            )
        else:
            prev = entity_zero

        if prev is None:
            return None

        prev = inspect(prev)
        attr = getattr(prev.entity, onclause, None)
        if attr is not None:
            return attr.property.entity
    # legacy ^^^^^^^^^^^^^^^^^^^^^^^^^^^

    return None


class _QueryEntity(object):
    """represent an entity column returned within a Query result."""

    __slots__ = ()

    _non_hashable_value = False
    _null_column_type = False
    use_id_for_hash = False

    @classmethod
    def to_compile_state(
        cls, compile_state, entities, entities_collection, is_current_entities
    ):

        for idx, entity in enumerate(entities):
            if entity._is_lambda_element:
                if entity._is_sequence:
                    cls.to_compile_state(
                        compile_state,
                        entity._resolved,
                        entities_collection,
                        is_current_entities,
                    )
                    continue
                else:
                    entity = entity._resolved

            if entity.is_clause_element:
                if entity.is_selectable:
                    if "parententity" in entity._annotations:
                        _MapperEntity(
                            compile_state,
                            entity,
                            entities_collection,
                            is_current_entities,
                        )
                    else:
                        _ColumnEntity._for_columns(
                            compile_state,
                            entity._select_iterable,
                            entities_collection,
                            idx,
                            is_current_entities,
                        )
                else:
                    if entity._annotations.get("bundle", False):
                        _BundleEntity(
                            compile_state,
                            entity,
                            entities_collection,
                            is_current_entities,
                        )
                    elif entity._is_clause_list:
                        # this is legacy only - test_composites.py
                        # test_query_cols_legacy
                        _ColumnEntity._for_columns(
                            compile_state,
                            entity._select_iterable,
                            entities_collection,
                            idx,
                            is_current_entities,
                        )
                    else:
                        _ColumnEntity._for_columns(
                            compile_state,
                            [entity],
                            entities_collection,
                            idx,
                            is_current_entities,
                        )
            elif entity.is_bundle:
                _BundleEntity(compile_state, entity, entities_collection)

        return entities_collection


class _MapperEntity(_QueryEntity):
    """mapper/class/AliasedClass entity"""

    __slots__ = (
        "expr",
        "mapper",
        "entity_zero",
        "is_aliased_class",
        "path",
        "_extra_entities",
        "_label_name",
        "_with_polymorphic_mappers",
        "selectable",
        "_polymorphic_discriminator",
    )

    def __init__(
        self, compile_state, entity, entities_collection, is_current_entities
    ):
        entities_collection.append(self)
        if is_current_entities:
            if compile_state._primary_entity is None:
                compile_state._primary_entity = self
            compile_state._has_mapper_entities = True
            compile_state._has_orm_entities = True

        entity = entity._annotations["parententity"]
        entity._post_inspect
        ext_info = self.entity_zero = entity
        entity = ext_info.entity

        self.expr = entity
        self.mapper = mapper = ext_info.mapper

        self._extra_entities = (self.expr,)

        if ext_info.is_aliased_class:
            self._label_name = ext_info.name
        else:
            self._label_name = mapper.class_.__name__

        self.is_aliased_class = ext_info.is_aliased_class
        self.path = ext_info._path_registry

        if ext_info in compile_state._with_polymorphic_adapt_map:
            # this codepath occurs only if query.with_polymorphic() were
            # used

            wp = inspect(compile_state._with_polymorphic_adapt_map[ext_info])

            if self.is_aliased_class:
                # TODO: invalidrequest ?
                raise NotImplementedError(
                    "Can't use with_polymorphic() against an Aliased object"
                )

            mappers, from_obj = mapper._with_polymorphic_args(
                wp.with_polymorphic_mappers, wp.selectable
            )

            self._with_polymorphic_mappers = mappers
            self.selectable = from_obj
            self._polymorphic_discriminator = wp.polymorphic_on

        else:
            self.selectable = ext_info.selectable
            self._with_polymorphic_mappers = ext_info.with_polymorphic_mappers
            self._polymorphic_discriminator = ext_info.polymorphic_on

            if mapper._should_select_with_poly_adapter:
                compile_state._create_with_polymorphic_adapter(
                    ext_info, self.selectable
                )

    supports_single_entity = True

    _non_hashable_value = True
    use_id_for_hash = True

    @property
    def type(self):
        return self.mapper.class_

    @property
    def entity_zero_or_selectable(self):
        return self.entity_zero

    def corresponds_to(self, entity):
        return _entity_corresponds_to(self.entity_zero, entity)

    def _get_entity_clauses(self, compile_state):

        adapter = None

        if not self.is_aliased_class:
            if compile_state._polymorphic_adapters:
                adapter = compile_state._polymorphic_adapters.get(
                    self.mapper, None
                )
        else:
            adapter = self.entity_zero._adapter

        if adapter:
            if compile_state._from_obj_alias:
                ret = adapter.wrap(compile_state._from_obj_alias)
            else:
                ret = adapter
        else:
            ret = compile_state._from_obj_alias

        return ret

    def row_processor(self, context, result):
        compile_state = context.compile_state
        adapter = self._get_entity_clauses(compile_state)

        if compile_state.compound_eager_adapter and adapter:
            adapter = adapter.wrap(compile_state.compound_eager_adapter)
        elif not adapter:
            adapter = compile_state.compound_eager_adapter

        if compile_state._primary_entity is self:
            only_load_props = compile_state.compile_options._only_load_props
            refresh_state = context.refresh_state
        else:
            only_load_props = refresh_state = None

        _instance = loading._instance_processor(
            self,
            self.mapper,
            context,
            result,
            self.path,
            adapter,
            only_load_props=only_load_props,
            refresh_state=refresh_state,
            polymorphic_discriminator=self._polymorphic_discriminator,
        )

        return _instance, self._label_name, self._extra_entities

    def setup_compile_state(self, compile_state):

        adapter = self._get_entity_clauses(compile_state)

        single_table_crit = self.mapper._single_table_criterion
        if (
            single_table_crit is not None
            or ("additional_entity_criteria", self.mapper)
            in compile_state.global_attributes
        ):
            ext_info = self.entity_zero
            compile_state.extra_criteria_entities[ext_info] = (
                ext_info,
                ext_info._adapter if ext_info.is_aliased_class else None,
            )

        loading._setup_entity_query(
            compile_state,
            self.mapper,
            self,
            self.path,
            adapter,
            compile_state.primary_columns,
            with_polymorphic=self._with_polymorphic_mappers,
            only_load_props=compile_state.compile_options._only_load_props,
            polymorphic_discriminator=self._polymorphic_discriminator,
        )

        compile_state._fallback_from_clauses.append(self.selectable)


class _BundleEntity(_QueryEntity):

    _extra_entities = ()

    __slots__ = (
        "bundle",
        "expr",
        "type",
        "_label_name",
        "_entities",
        "supports_single_entity",
    )

    def __init__(
        self,
        compile_state,
        expr,
        entities_collection,
        is_current_entities,
        setup_entities=True,
        parent_bundle=None,
    ):
        compile_state._has_orm_entities = True

        expr = expr._annotations["bundle"]
        if parent_bundle:
            parent_bundle._entities.append(self)
        else:
            entities_collection.append(self)

        if isinstance(
            expr, (attributes.QueryableAttribute, interfaces.PropComparator)
        ):
            bundle = expr.__clause_element__()
        else:
            bundle = expr

        self.bundle = self.expr = bundle
        self.type = type(bundle)
        self._label_name = bundle.name
        self._entities = []

        if setup_entities:
            for expr in bundle.exprs:
                if "bundle" in expr._annotations:
                    _BundleEntity(
                        compile_state,
                        expr,
                        entities_collection,
                        is_current_entities,
                        parent_bundle=self,
                    )
                elif isinstance(expr, Bundle):
                    _BundleEntity(
                        compile_state,
                        expr,
                        entities_collection,
                        is_current_entities,
                        parent_bundle=self,
                    )
                else:
                    _ORMColumnEntity._for_columns(
                        compile_state,
                        [expr],
                        entities_collection,
                        None,
                        is_current_entities,
                        parent_bundle=self,
                    )

        self.supports_single_entity = self.bundle.single_entity
        if (
            self.supports_single_entity
            and not compile_state.compile_options._use_legacy_query_style
        ):
            util.warn_deprecated_20(
                "The Bundle.single_entity flag has no effect when "
                "using 2.0 style execution."
            )

    @property
    def mapper(self):
        ezero = self.entity_zero
        if ezero is not None:
            return ezero.mapper
        else:
            return None

    @property
    def entity_zero(self):
        for ent in self._entities:
            ezero = ent.entity_zero
            if ezero is not None:
                return ezero
        else:
            return None

    def corresponds_to(self, entity):
        # TODO: we might be able to implement this but for now
        # we are working around it
        return False

    @property
    def entity_zero_or_selectable(self):
        for ent in self._entities:
            ezero = ent.entity_zero_or_selectable
            if ezero is not None:
                return ezero
        else:
            return None

    def setup_compile_state(self, compile_state):
        for ent in self._entities:
            ent.setup_compile_state(compile_state)

    def row_processor(self, context, result):
        procs, labels, extra = zip(
            *[ent.row_processor(context, result) for ent in self._entities]
        )

        proc = self.bundle.create_row_processor(context.query, procs, labels)

        return proc, self._label_name, self._extra_entities


class _ColumnEntity(_QueryEntity):
    __slots__ = (
        "_fetch_column",
        "_row_processor",
        "raw_column_index",
        "translate_raw_column",
    )

    @classmethod
    def _for_columns(
        cls,
        compile_state,
        columns,
        entities_collection,
        raw_column_index,
        is_current_entities,
        parent_bundle=None,
    ):
        for column in columns:
            annotations = column._annotations
            if "parententity" in annotations:
                _entity = annotations["parententity"]
            else:
                _entity = sql_util.extract_first_column_annotation(
                    column, "parententity"
                )

            if _entity:
                if "identity_token" in column._annotations:
                    _IdentityTokenEntity(
                        compile_state,
                        column,
                        entities_collection,
                        _entity,
                        raw_column_index,
                        is_current_entities,
                        parent_bundle=parent_bundle,
                    )
                else:
                    _ORMColumnEntity(
                        compile_state,
                        column,
                        entities_collection,
                        _entity,
                        raw_column_index,
                        is_current_entities,
                        parent_bundle=parent_bundle,
                    )
            else:
                _RawColumnEntity(
                    compile_state,
                    column,
                    entities_collection,
                    raw_column_index,
                    is_current_entities,
                    parent_bundle=parent_bundle,
                )

    @property
    def type(self):
        return self.column.type

    @property
    def _non_hashable_value(self):
        return not self.column.type.hashable

    @property
    def _null_column_type(self):
        return self.column.type._isnull

    def row_processor(self, context, result):
        compile_state = context.compile_state

        # the resulting callable is entirely cacheable so just return
        # it if we already made one
        if self._row_processor is not None:
            getter, label_name, extra_entities = self._row_processor
            if self.translate_raw_column:
                extra_entities += (
                    result.context.invoked_statement._raw_columns[
                        self.raw_column_index
                    ],
                )

            return getter, label_name, extra_entities

        # retrieve the column that would have been set up in
        # setup_compile_state, to avoid doing redundant work
        if self._fetch_column is not None:
            column = self._fetch_column
        else:
            # fetch_column will be None when we are doing a from_statement
            # and setup_compile_state may not have been called.
            column = self.column

            # previously, the RawColumnEntity didn't look for from_obj_alias
            # however I can't think of a case where we would be here and
            # we'd want to ignore it if this is the from_statement use case.
            # it's not really a use case to have raw columns + from_statement
            if compile_state._from_obj_alias:
                column = compile_state._from_obj_alias.columns[column]

            if column._annotations:
                # annotated columns perform more slowly in compiler and
                # result due to the __eq__() method, so use deannotated
                column = column._deannotate()

        if compile_state.compound_eager_adapter:
            column = compile_state.compound_eager_adapter.columns[column]

        getter = result._getter(column)

        ret = getter, self._label_name, self._extra_entities
        self._row_processor = ret

        if self.translate_raw_column:
            extra_entities = self._extra_entities + (
                result.context.invoked_statement._raw_columns[
                    self.raw_column_index
                ],
            )
            return getter, self._label_name, extra_entities
        else:
            return ret


class _RawColumnEntity(_ColumnEntity):
    entity_zero = None
    mapper = None
    supports_single_entity = False

    __slots__ = (
        "expr",
        "column",
        "_label_name",
        "entity_zero_or_selectable",
        "_extra_entities",
    )

    def __init__(
        self,
        compile_state,
        column,
        entities_collection,
        raw_column_index,
        is_current_entities,
        parent_bundle=None,
    ):
        self.expr = column
        self.raw_column_index = raw_column_index
        self.translate_raw_column = raw_column_index is not None

        if column._is_star:
            compile_state.compile_options += {"_is_star": True}

        if not is_current_entities or column._is_text_clause:
            self._label_name = None
        else:
            self._label_name = compile_state._label_convention(column)

        if parent_bundle:
            parent_bundle._entities.append(self)
        else:
            entities_collection.append(self)

        self.column = column
        self.entity_zero_or_selectable = (
            self.column._from_objects[0] if self.column._from_objects else None
        )
        self._extra_entities = (self.expr, self.column)
        self._fetch_column = self._row_processor = None

    def corresponds_to(self, entity):
        return False

    def setup_compile_state(self, compile_state):
        current_adapter = compile_state._get_current_adapter()
        if current_adapter:
            column = current_adapter(self.column, False)
        else:
            column = self.column

        if column._annotations:
            # annotated columns perform more slowly in compiler and
            # result due to the __eq__() method, so use deannotated
            column = column._deannotate()

        compile_state.dedupe_columns.add(column)
        compile_state.primary_columns.append(column)
        self._fetch_column = column


class _ORMColumnEntity(_ColumnEntity):
    """Column/expression based entity."""

    supports_single_entity = False

    __slots__ = (
        "expr",
        "mapper",
        "column",
        "_label_name",
        "entity_zero_or_selectable",
        "entity_zero",
        "_extra_entities",
    )

    def __init__(
        self,
        compile_state,
        column,
        entities_collection,
        parententity,
        raw_column_index,
        is_current_entities,
        parent_bundle=None,
    ):
        annotations = column._annotations

        _entity = parententity

        # an AliasedClass won't have proxy_key in the annotations for
        # a column if it was acquired using the class' adapter directly,
        # such as using AliasedInsp._adapt_element().  this occurs
        # within internal loaders.

        orm_key = annotations.get("proxy_key", None)
        proxy_owner = annotations.get("proxy_owner", _entity)
        if orm_key:
            self.expr = getattr(proxy_owner.entity, orm_key)
            self.translate_raw_column = False
        else:
            # if orm_key is not present, that means this is an ad-hoc
            # SQL ColumnElement, like a CASE() or other expression.
            # include this column position from the invoked statement
            # in the ORM-level ResultSetMetaData on each execute, so that
            # it can be targeted by identity after caching
            self.expr = column
            self.translate_raw_column = raw_column_index is not None

        self.raw_column_index = raw_column_index

        if is_current_entities:
            self._label_name = compile_state._label_convention(
                column, col_name=orm_key
            )
        else:
            self._label_name = None

        _entity._post_inspect
        self.entity_zero = self.entity_zero_or_selectable = ezero = _entity
        self.mapper = mapper = _entity.mapper

        if parent_bundle:
            parent_bundle._entities.append(self)
        else:
            entities_collection.append(self)

        compile_state._has_orm_entities = True

        self.column = column

        self._fetch_column = self._row_processor = None

        self._extra_entities = (self.expr, self.column)

        if mapper._should_select_with_poly_adapter:
            compile_state._create_with_polymorphic_adapter(
                ezero, ezero.selectable
            )

    def corresponds_to(self, entity):
        if _is_aliased_class(entity):
            # TODO: polymorphic subclasses ?
            return entity is self.entity_zero
        else:
            return not _is_aliased_class(
                self.entity_zero
            ) and entity.common_parent(self.entity_zero)

    def setup_compile_state(self, compile_state):
        current_adapter = compile_state._get_current_adapter()
        if current_adapter:
            column = current_adapter(self.column, False)
        else:
            column = self.column

        ezero = self.entity_zero

        single_table_crit = self.mapper._single_table_criterion
        if (
            single_table_crit is not None
            or ("additional_entity_criteria", self.mapper)
            in compile_state.global_attributes
        ):

            compile_state.extra_criteria_entities[ezero] = (
                ezero,
                ezero._adapter if ezero.is_aliased_class else None,
            )

        if column._annotations and not column._expression_label:
            # annotated columns perform more slowly in compiler and
            # result due to the __eq__() method, so use deannotated
            column = column._deannotate()

        # use entity_zero as the from if we have it. this is necessary
        # for polymorphic scenarios where our FROM is based on ORM entity,
        # not the FROM of the column.  but also, don't use it if our column
        # doesn't actually have any FROMs that line up, such as when its
        # a scalar subquery.
        if set(self.column._from_objects).intersection(
            ezero.selectable._from_objects
        ):
            compile_state._fallback_from_clauses.append(ezero.selectable)

        compile_state.dedupe_columns.add(column)
        compile_state.primary_columns.append(column)
        self._fetch_column = column


class _IdentityTokenEntity(_ORMColumnEntity):
    translate_raw_column = False

    def setup_compile_state(self, compile_state):
        pass

    def row_processor(self, context, result):
        def getter(row):
            return context.load_options._refresh_identity_token

        return getter, self._label_name, self._extra_entities
