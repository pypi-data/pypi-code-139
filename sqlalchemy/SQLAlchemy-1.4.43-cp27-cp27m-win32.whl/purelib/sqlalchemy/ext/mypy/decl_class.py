# ext/mypy/decl_class.py
# Copyright (C) 2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

from typing import List
from typing import Optional
from typing import Union

from mypy.nodes import AssignmentStmt
from mypy.nodes import CallExpr
from mypy.nodes import ClassDef
from mypy.nodes import Decorator
from mypy.nodes import LambdaExpr
from mypy.nodes import ListExpr
from mypy.nodes import MemberExpr
from mypy.nodes import NameExpr
from mypy.nodes import PlaceholderNode
from mypy.nodes import RefExpr
from mypy.nodes import StrExpr
from mypy.nodes import SymbolNode
from mypy.nodes import SymbolTableNode
from mypy.nodes import TempNode
from mypy.nodes import TypeInfo
from mypy.nodes import Var
from mypy.plugin import SemanticAnalyzerPluginInterface
from mypy.types import AnyType
from mypy.types import CallableType
from mypy.types import get_proper_type
from mypy.types import Instance
from mypy.types import NoneType
from mypy.types import ProperType
from mypy.types import Type
from mypy.types import TypeOfAny
from mypy.types import UnboundType
from mypy.types import UnionType

from . import apply
from . import infer
from . import names
from . import util


def scan_declarative_assignments_and_apply_types(
    cls: ClassDef,
    api: SemanticAnalyzerPluginInterface,
    is_mixin_scan: bool = False,
) -> Optional[List[util.SQLAlchemyAttribute]]:

    info = util.info_for_cls(cls, api)

    if info is None:
        # this can occur during cached passes
        return None
    elif cls.fullname.startswith("builtins"):
        return None

    mapped_attributes: Optional[
        List[util.SQLAlchemyAttribute]
    ] = util.get_mapped_attributes(info, api)

    # used by assign.add_additional_orm_attributes among others
    util.establish_as_sqlalchemy(info)

    if mapped_attributes is not None:
        # ensure that a class that's mapped is always picked up by
        # its mapped() decorator or declarative metaclass before
        # it would be detected as an unmapped mixin class

        if not is_mixin_scan:
            # mypy can call us more than once.  it then *may* have reset the
            # left hand side of everything, but not the right that we removed,
            # removing our ability to re-scan.   but we have the types
            # here, so lets re-apply them, or if we have an UnboundType,
            # we can re-scan

            apply.re_apply_declarative_assignments(cls, api, mapped_attributes)

        return mapped_attributes

    mapped_attributes = []

    if not cls.defs.body:
        # when we get a mixin class from another file, the body is
        # empty (!) but the names are in the symbol table.  so use that.

        for sym_name, sym in info.names.items():
            _scan_symbol_table_entry(
                cls, api, sym_name, sym, mapped_attributes
            )
    else:
        for stmt in util.flatten_typechecking(cls.defs.body):
            if isinstance(stmt, AssignmentStmt):
                _scan_declarative_assignment_stmt(
                    cls, api, stmt, mapped_attributes
                )
            elif isinstance(stmt, Decorator):
                _scan_declarative_decorator_stmt(
                    cls, api, stmt, mapped_attributes
                )
    _scan_for_mapped_bases(cls, api)

    if not is_mixin_scan:
        apply.add_additional_orm_attributes(cls, api, mapped_attributes)

    util.set_mapped_attributes(info, mapped_attributes)

    return mapped_attributes


def _scan_symbol_table_entry(
    cls: ClassDef,
    api: SemanticAnalyzerPluginInterface,
    name: str,
    value: SymbolTableNode,
    attributes: List[util.SQLAlchemyAttribute],
) -> None:
    """Extract mapping information from a SymbolTableNode that's in the
    type.names dictionary.

    """
    value_type = get_proper_type(value.type)
    if not isinstance(value_type, Instance):
        return

    left_hand_explicit_type = None
    type_id = names.type_id_for_named_node(value_type.type)
    # type_id = names._type_id_for_unbound_type(value.type.type, cls, api)

    err = False

    # TODO: this is nearly the same logic as that of
    # _scan_declarative_decorator_stmt, likely can be merged
    if type_id in {
        names.MAPPED,
        names.RELATIONSHIP,
        names.COMPOSITE_PROPERTY,
        names.MAPPER_PROPERTY,
        names.SYNONYM_PROPERTY,
        names.COLUMN_PROPERTY,
    }:
        if value_type.args:
            left_hand_explicit_type = get_proper_type(value_type.args[0])
        else:
            err = True
    elif type_id is names.COLUMN:
        if not value_type.args:
            err = True
        else:
            typeengine_arg: Union[ProperType, TypeInfo] = get_proper_type(
                value_type.args[0]
            )
            if isinstance(typeengine_arg, Instance):
                typeengine_arg = typeengine_arg.type

            if isinstance(typeengine_arg, (UnboundType, TypeInfo)):
                sym = api.lookup_qualified(typeengine_arg.name, typeengine_arg)
                if sym is not None and isinstance(sym.node, TypeInfo):
                    if names.has_base_type_id(sym.node, names.TYPEENGINE):

                        left_hand_explicit_type = UnionType(
                            [
                                infer.extract_python_type_from_typeengine(
                                    api, sym.node, []
                                ),
                                NoneType(),
                            ]
                        )
                    else:
                        util.fail(
                            api,
                            "Column type should be a TypeEngine "
                            "subclass not '{}'".format(sym.node.fullname),
                            value_type,
                        )

    if err:
        msg = (
            "Can't infer type from attribute {} on class {}. "
            "please specify a return type from this function that is "
            "one of: Mapped[<python type>], relationship[<target class>], "
            "Column[<TypeEngine>], MapperProperty[<python type>]"
        )
        util.fail(api, msg.format(name, cls.name), cls)

        left_hand_explicit_type = AnyType(TypeOfAny.special_form)

    if left_hand_explicit_type is not None:
        assert value.node is not None
        attributes.append(
            util.SQLAlchemyAttribute(
                name=name,
                line=value.node.line,
                column=value.node.column,
                typ=left_hand_explicit_type,
                info=cls.info,
            )
        )


def _scan_declarative_decorator_stmt(
    cls: ClassDef,
    api: SemanticAnalyzerPluginInterface,
    stmt: Decorator,
    attributes: List[util.SQLAlchemyAttribute],
) -> None:
    """Extract mapping information from a @declared_attr in a declarative
    class.

    E.g.::

        @reg.mapped
        class MyClass:
            # ...

            @declared_attr
            def updated_at(cls) -> Column[DateTime]:
                return Column(DateTime)

    Will resolve in mypy as::

        @reg.mapped
        class MyClass:
            # ...

            updated_at: Mapped[Optional[datetime.datetime]]

    """
    for dec in stmt.decorators:
        if (
            isinstance(dec, (NameExpr, MemberExpr, SymbolNode))
            and names.type_id_for_named_node(dec) is names.DECLARED_ATTR
        ):
            break
    else:
        return

    dec_index = cls.defs.body.index(stmt)

    left_hand_explicit_type: Optional[ProperType] = None

    if util.name_is_dunder(stmt.name):
        # for dunder names like __table_args__, __tablename__,
        # __mapper_args__ etc., rewrite these as simple assignment
        # statements; otherwise mypy doesn't like if the decorated
        # function has an annotation like ``cls: Type[Foo]`` because
        # it isn't @classmethod
        any_ = AnyType(TypeOfAny.special_form)
        left_node = NameExpr(stmt.var.name)
        left_node.node = stmt.var
        new_stmt = AssignmentStmt([left_node], TempNode(any_))
        new_stmt.type = left_node.node.type
        cls.defs.body[dec_index] = new_stmt
        return
    elif isinstance(stmt.func.type, CallableType):
        func_type = stmt.func.type.ret_type
        if isinstance(func_type, UnboundType):
            type_id = names.type_id_for_unbound_type(func_type, cls, api)
        else:
            # this does not seem to occur unless the type argument is
            # incorrect
            return

        if (
            type_id
            in {
                names.MAPPED,
                names.RELATIONSHIP,
                names.COMPOSITE_PROPERTY,
                names.MAPPER_PROPERTY,
                names.SYNONYM_PROPERTY,
                names.COLUMN_PROPERTY,
            }
            and func_type.args
        ):
            left_hand_explicit_type = get_proper_type(func_type.args[0])
        elif type_id is names.COLUMN and func_type.args:
            typeengine_arg = func_type.args[0]
            if isinstance(typeengine_arg, UnboundType):
                sym = api.lookup_qualified(typeengine_arg.name, typeengine_arg)
                if sym is not None and isinstance(sym.node, TypeInfo):
                    if names.has_base_type_id(sym.node, names.TYPEENGINE):
                        left_hand_explicit_type = UnionType(
                            [
                                infer.extract_python_type_from_typeengine(
                                    api, sym.node, []
                                ),
                                NoneType(),
                            ]
                        )
                    else:
                        util.fail(
                            api,
                            "Column type should be a TypeEngine "
                            "subclass not '{}'".format(sym.node.fullname),
                            func_type,
                        )

    if left_hand_explicit_type is None:
        # no type on the decorated function.  our option here is to
        # dig into the function body and get the return type, but they
        # should just have an annotation.
        msg = (
            "Can't infer type from @declared_attr on function '{}';  "
            "please specify a return type from this function that is "
            "one of: Mapped[<python type>], relationship[<target class>], "
            "Column[<TypeEngine>], MapperProperty[<python type>]"
        )
        util.fail(api, msg.format(stmt.var.name), stmt)

        left_hand_explicit_type = AnyType(TypeOfAny.special_form)

    left_node = NameExpr(stmt.var.name)
    left_node.node = stmt.var

    # totally feeling around in the dark here as I don't totally understand
    # the significance of UnboundType.  It seems to be something that is
    # not going to do what's expected when it is applied as the type of
    # an AssignmentStatement.  So do a feeling-around-in-the-dark version
    # of converting it to the regular Instance/TypeInfo/UnionType structures
    # we see everywhere else.
    if isinstance(left_hand_explicit_type, UnboundType):
        left_hand_explicit_type = get_proper_type(
            util.unbound_to_instance(api, left_hand_explicit_type)
        )

    left_node.node.type = api.named_type(
        names.NAMED_TYPE_SQLA_MAPPED, [left_hand_explicit_type]
    )

    # this will ignore the rvalue entirely
    # rvalue = TempNode(AnyType(TypeOfAny.special_form))

    # rewrite the node as:
    # <attr> : Mapped[<typ>] =
    # _sa_Mapped._empty_constructor(lambda: <function body>)
    # the function body is maintained so it gets type checked internally
    rvalue = util.expr_to_mapped_constructor(
        LambdaExpr(stmt.func.arguments, stmt.func.body)
    )

    new_stmt = AssignmentStmt([left_node], rvalue)
    new_stmt.type = left_node.node.type

    attributes.append(
        util.SQLAlchemyAttribute(
            name=left_node.name,
            line=stmt.line,
            column=stmt.column,
            typ=left_hand_explicit_type,
            info=cls.info,
        )
    )
    cls.defs.body[dec_index] = new_stmt


def _scan_declarative_assignment_stmt(
    cls: ClassDef,
    api: SemanticAnalyzerPluginInterface,
    stmt: AssignmentStmt,
    attributes: List[util.SQLAlchemyAttribute],
) -> None:
    """Extract mapping information from an assignment statement in a
    declarative class.

    """
    lvalue = stmt.lvalues[0]
    if not isinstance(lvalue, NameExpr):
        return

    sym = cls.info.names.get(lvalue.name)

    # this establishes that semantic analysis has taken place, which
    # means the nodes are populated and we are called from an appropriate
    # hook.
    assert sym is not None
    node = sym.node

    if isinstance(node, PlaceholderNode):
        return

    assert node is lvalue.node
    assert isinstance(node, Var)

    if node.name == "__abstract__":
        if api.parse_bool(stmt.rvalue) is True:
            util.set_is_base(cls.info)
        return
    elif node.name == "__tablename__":
        util.set_has_table(cls.info)
    elif node.name.startswith("__"):
        return
    elif node.name == "_mypy_mapped_attrs":
        if not isinstance(stmt.rvalue, ListExpr):
            util.fail(api, "_mypy_mapped_attrs is expected to be a list", stmt)
        else:
            for item in stmt.rvalue.items:
                if isinstance(item, (NameExpr, StrExpr)):
                    apply.apply_mypy_mapped_attr(cls, api, item, attributes)

    left_hand_mapped_type: Optional[Type] = None
    left_hand_explicit_type: Optional[ProperType] = None

    if node.is_inferred or node.type is None:
        if isinstance(stmt.type, UnboundType):
            # look for an explicit Mapped[] type annotation on the left
            # side with nothing on the right

            # print(stmt.type)
            # Mapped?[Optional?[A?]]

            left_hand_explicit_type = stmt.type

            if stmt.type.name == "Mapped":
                mapped_sym = api.lookup_qualified("Mapped", cls)
                if (
                    mapped_sym is not None
                    and mapped_sym.node is not None
                    and names.type_id_for_named_node(mapped_sym.node)
                    is names.MAPPED
                ):
                    left_hand_explicit_type = get_proper_type(
                        stmt.type.args[0]
                    )
                    left_hand_mapped_type = stmt.type

            # TODO: do we need to convert from unbound for this case?
            # left_hand_explicit_type = util._unbound_to_instance(
            #     api, left_hand_explicit_type
            # )
    else:
        node_type = get_proper_type(node.type)
        if (
            isinstance(node_type, Instance)
            and names.type_id_for_named_node(node_type.type) is names.MAPPED
        ):
            # print(node.type)
            # sqlalchemy.orm.attributes.Mapped[<python type>]
            left_hand_explicit_type = get_proper_type(node_type.args[0])
            left_hand_mapped_type = node_type
        else:
            # print(node.type)
            # <python type>
            left_hand_explicit_type = node_type
            left_hand_mapped_type = None

    if isinstance(stmt.rvalue, TempNode) and left_hand_mapped_type is not None:
        # annotation without assignment and Mapped is present
        # as type annotation
        # equivalent to using _infer_type_from_left_hand_type_only.

        python_type_for_type = left_hand_explicit_type
    elif isinstance(stmt.rvalue, CallExpr) and isinstance(
        stmt.rvalue.callee, RefExpr
    ):

        python_type_for_type = infer.infer_type_from_right_hand_nameexpr(
            api, stmt, node, left_hand_explicit_type, stmt.rvalue.callee
        )

        if python_type_for_type is None:
            return

    else:
        return

    assert python_type_for_type is not None

    attributes.append(
        util.SQLAlchemyAttribute(
            name=node.name,
            line=stmt.line,
            column=stmt.column,
            typ=python_type_for_type,
            info=cls.info,
        )
    )

    apply.apply_type_to_mapped_statement(
        api,
        stmt,
        lvalue,
        left_hand_explicit_type,
        python_type_for_type,
    )


def _scan_for_mapped_bases(
    cls: ClassDef,
    api: SemanticAnalyzerPluginInterface,
) -> None:
    """Given a class, iterate through its superclass hierarchy to find
    all other classes that are considered as ORM-significant.

    Locates non-mapped mixins and scans them for mapped attributes to be
    applied to subclasses.

    """

    info = util.info_for_cls(cls, api)

    if info is None:
        return

    for base_info in info.mro[1:-1]:
        if base_info.fullname.startswith("builtins"):
            continue

        # scan each base for mapped attributes.  if they are not already
        # scanned (but have all their type info), that means they are unmapped
        # mixins
        scan_declarative_assignments_and_apply_types(
            base_info.defn, api, is_mixin_scan=True
        )
